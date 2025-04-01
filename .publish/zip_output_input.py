# create a zip file for the output of the MIKE21HD-Oresund model

import zipfile


def zip_output(fn):
    with zipfile.ZipFile(fn, "w") as z:
        path_output = r"\\DKCPH1-STOR.DHI.DK\Projects\11561006\WaterBench\WaterBench-MIKE21HD-SouthernNorthSea\MIKE21HD-SouthernNorthSea-output"
        path_output = "output"
        z.write(path_output + "/Area.dfsu",arcname="Area.dfsu")
        z.write(path_output + "/Points.dfs0",arcname="Points.dfs0")
        z.write(".publish/README_output.md",arcname="README.md")
    print(f"Zip file created: {fn}")

def zip_input(fn):
    with zipfile.ZipFile(fn, "w") as z:
        path_input = r"\\DKCPH1-STOR.DHI.DK\Projects\11561006\WaterBench\WaterBench-MIKE21HD-SouthernNorthSea\MIKE21HD-SouthernNorthSea-input"
        path_input = "input"
        z.write(path_input + "/wind.dfs2",arcname="wind.dfs2")
        z.write(".publish/README_input.md",arcname="README.md")
    print(f"Zip file created: {fn}")

if __name__ == "__main__":
    zip_output(fn=".publish/MIKE21HD-SouthernNorthSea-output.zip")
    zip_input(fn=".publish/MIKE21HD-SouthernNorthSea-input.zip")
