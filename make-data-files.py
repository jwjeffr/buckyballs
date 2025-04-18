from tempfile import NamedTemporaryFile

import requests
from ase.io import read, write
import numpy as np


SYSTEMS = {
    "c60-ih": "https://nanotube.msu.edu/fullerene/C60/C60-Ih.xyz"
}


def main():

    for system, url in SYSTEMS.items():

        with NamedTemporaryFile(mode="w+") as file:
            file.write(requests.get(url).content.decode("utf-8"))
            file.seek(0)
            atoms = read(file, format="xyz")
        
        atoms.translate(
            -atoms.get_positions().min(axis=0)
        )
        atoms.set_cell(
            1.25 * np.diag(atoms.get_positions().max(axis=0))
        )

        supercell = atoms.repeat((2, 2, 2))
        write(f"data-files/{system}.dat", supercell, format="lammps-data")


if __name__ == "__main__":

    main()
