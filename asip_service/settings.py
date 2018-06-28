import logging

# Logger settings
logging.root.handlers = []

FORMAT = '%(asctime)s : %(levelname)s : %(message)s\r'

logging.basicConfig(format=FORMAT, level=logging.DEBUG,
                    filename='logs.log')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)  # this is only if we want to error logs be printed out to console

# Set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s : [%(filename)s:%(lineno)d] : %(levelname)s - %(message)s','%m-%d %H:%M:%S')

console.setFormatter(formatter)
logging.getLogger("").addHandler(console)
