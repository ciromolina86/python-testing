import s3_volta_files

framerate, df_data = s3_volta_files.parse_file(filename='C:/Users/cmolina/PycharmProjects/my-scripts/Node_21000_20210202_000000_1612224000.esa')
print(df_data.head())

