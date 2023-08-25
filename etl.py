import pandas as pd
import sys

#This program reads the raw excel file into a pandas dataframe, and drops the rows we do not want
#whether you want to do a .xls file or a .csv file you must specify manually in #create_dataframe!
# also if you want to drop a column you need to specify manually!
def create_dataframe(input_file, dropbelow, dropabove):
    try:
        # skip the first 6 rows
        dropabove_int = int(dropabove)
        dropbelow_int = int(dropbelow)

        df = pd.read_csv(input_file, skiprows=lambda x: x < dropbelow_int or x > dropabove_int)

        # Drop the column named " high " if it exists, can be replaced with anything
        if "high" in df.columns:
            df = df.drop(columns=["high"])

        return df
    except FileNotFoundError:
        print("not  found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("python etl.py inputfile.xls number number")
        sys.exit(1)

    input_file = sys.argv[1]
    dropbelow = sys.argv[2]
    dropabove = sys.argv[3]
    df = create_dataframe(input_file, dropbelow, dropabove)


    # save the dataframe
    output_file = "output_dataframe.csv"
    df.to_csv(output_file, index=False)
    print(f" saved as '{output_file}'")