# create a zip file for the output of the MIKE21HD-Oresund model

import zipfile

zip_fn = ".publish/MIKE21HD-ConceptionBay-output.zip"


def zip_repo():
    with zipfile.ZipFile(zip_fn, "w") as z:
        path_output = r"\\DKCPH1-STOR.DHI.DK\Projects\11560605\BenchmarkCases\WaterBench-MIKE21HD-ConceptionBay\MIKE21HD-ConceptionBay-output"
        z.write(path_output + "/Area_2014_2018.dfsu",arcname="Area_2014_2018.dfsu")
        z.write(path_output + "/Area_2019_2022.dfsu",arcname="Area_2019_2022.dfsu")
        z.write(path_output + "/Points.dfs0",arcname="Points.dfs0")
        z.write(".publish/README_output.md",arcname="README.md")
    print(f"Zip file created: {zip_fn}")

if __name__ == "__main__":
    zip_repo()
