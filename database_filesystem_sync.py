import argparse
import logging
import pathlib


class DatabaseFilesystemSync:
    def __init__(self, root, db_user, db_host, db_password):
        self.root = root
        self.db_user = db_user
        self.db_host = db_host
        self.db_password = db_password

    def sync(self, dry_run=False):
        files = self.scan_files()
        db_entries = self.read_db_entries()
        required_updates = self.determine_updates(files, db_entries)
        if dry_run is True:
            logging.warning(
                f'Required Adds: {len(required_updates["adds"])}, '
                'required Deletes: {len(required_updates["deletes"])}, but in DRY_RUN mode'
            )
        else:
            self.do_updates(required_updates)

    def scan_files(self):
        ret = []
        for child in self.root.rglob("*"):
            if not child.is_file():
                continue
            if not len(child.relative_to(self.root).parents) == 3:
                logging.warning(
                    f"Skipping {child} as not expected # of directories deep"
                )
                continue
            ret.append(child)
        logging.info(f"Found {len(ret)} files")
        return ret

    def read_db_entries(self):
        # to be implemented
        pass

    def determine_updates(self, files, db_entries):
        # to be implemented
        adds, deletes = [], []
        return dict(adds=adds, deletes=deletes)

    def do_updates(self, updates):
        # to be implemented
        pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root")
    parser.add_argument(
        "-d",
        "--dryrun",
        dest="dry_run",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument("--db_host")
    parser.add_argument("--db_user")
    parser.add_argument("--db_password")
    parser.add_argument(
        "-q",
        "--quiet",
        help="Only warnings or errors",
        action="store_const",
        dest="loglevel",
        const=logging.WARNING,
        default=logging.INFO,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    return parser.parse_args()


def main(args):
    root = pathlib.Path(args.root).expanduser()
    syncer = DatabaseFilesystemSync(root, args.db_host, args.db_user, args.db_password)
    syncer.sync(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    args = parse_args()
    logging.basicConfig(level=args.loglevel)
    raise SystemExit(main(args))
