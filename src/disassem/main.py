"""
Handle command line processing concerns
"""
import click
from address import Address
from rom import ROM


@click.command()
@click.option(
        "--rom",
        help="ROM file to disassemble",
        type=click.Path(exists=True),
        required=True
)
@click.option(
        "--listing",
        help="listing file to generate",
        type=click.Path(exists=False),
        required=True
)
@click.option(
        "--aorg",
        default="0x0000",
        help="the address of the first byte in the input ROM. Specified in hex such as 0x0000",
        type=Address
)
@click.option(
        "--cpu",
        default="9900",
        help="cpu type, one of 9900 or 9995. Defaults to 9900",
        type=str
)
@click.version_option(
        version="0.1",
        prog_name="9900dis"
)
def main(rom, listing, aorg, cpu):
    """TMS9900 disassembler by Jedimatt42"""
    
    disassembler = ROM(rom, listing, aorg, cpu == "9995")
    disassembler.disassemble()


if __name__ == "__main__":
    main()
