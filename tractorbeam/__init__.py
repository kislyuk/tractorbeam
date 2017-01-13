"""
Tractor Beam: File I/O staging for JSON documents with Amazon S3 URLs
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys, argparse, logging, json, datetime, traceback, errno
import boto3
from botocore.exceptions import NoRegionError
from tweak import Config
from .compat import str, urlparse

logger = logging.getLogger(__name__)
config = Config("tractorbeam")
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--log-level", type=logger.setLevel,
                    help=str([logging.getLevelName(i) for i in range(0, 60, 10)]),
                    default=logging.WARN)
subparsers = parser.add_subparsers()

s3 = boto3.resource("s3")

def register_parser(function, **add_parser_args):
    subparser = subparsers.add_parser(function.__name__, **add_parser_args)
    subparser.set_defaults(entry_point=function)
    if subparser.description is None:
        subparser.description = add_parser_args.get("help", function.__doc__)
    return subparser

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = parser.parse_args(args=args)
    try:
        result = parsed_args.entry_point(parsed_args)
    except Exception as e:
        if isinstance(e, NoRegionError):
            msg = "The AWS CLI is not configured."
            msg += " Please configure it using instructions at"
            msg += " http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html"
            exit(msg)
        elif logger.level < logging.ERROR:
            raise
        else:
            err_msg = traceback.format_exc()
            try:
                err_log_filename = os.path.join(config.user_config_dir, "error.log")
                with open(err_log_filename, "ab") as fh:
                    print(datetime.datetime.now().isoformat(), file=fh)
                    print(err_msg, file=fh)
                exit("{}: {}. See {} for error details.".format(e.__class__.__name__, e, err_log_filename))
            except Exception:
                print(err_msg, file=sys.stderr)
                exit(os.EX_SOFTWARE)
    if isinstance(result, SystemExit):
        raise result
    elif result is not None:
        if isinstance(result, dict) and "ResponseMetadata" in result:
            del result["ResponseMetadata"]
        print(json.dumps(result, indent=2, default=lambda x: str(x)))

def visit(node, prefix, transform, **kwargs):
    if isinstance(node, list):
        for i, value in enumerate(node):
            node[i] = visit(value, prefix, transform, **kwargs)
    elif isinstance(node, dict):
        for key, value in node.items():
            node[key] = visit(value, prefix, transform, **kwargs)
    else:
        if isinstance(node, str) and node.startswith(prefix):
            node = transform(node, **kwargs)
    return node

def process_s3_url(url, strip=0):
    url = urlparse(url)
    path = url.path.lstrip("/")
    dest = os.path.join(os.getcwd(), path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    s3.Object(url.netloc, path).download_file(dest)
    return "file://" + dest

def down(args):
    data = json.load(sys.stdin)
    return visit(data, "s3://", process_s3_url, strip=args.strip_components)

parser_down = register_parser(down)
parser_down.add_argument("--strip-components", type=int)

def process_file_url(url, dest_base, strip=0):
    url = urlparse(url)
    dest_base = urlparse(dest_base)
    dest = os.path.join(dest_base.path.lstrip("/"), url.path.lstrip("/"))
    s3.Object(dest_base.netloc, dest).upload_file(url.path)
    return "s3://" + os.path.join(dest_base.netloc, dest)

def up(args):
    data = json.load(sys.stdin)
    return visit(data, "file://", process_file_url, dest_base=args.dest_s3_base_url, strip=args.strip_components)

parser_up = register_parser(up)
parser_up.add_argument("dest_s3_base_url")
parser_up.add_argument("--strip-components", type=int)
