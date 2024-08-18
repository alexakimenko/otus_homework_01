from argparse import ArgumentParser

from src.app.process import main

CONFIG_PATH = "./configs/config.yaml"


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--config", help="config path")
    args = arg_parser.parse_args()

    config_path = args.config if args.config else CONFIG_PATH
    main(config_path)
