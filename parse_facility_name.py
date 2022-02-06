import os

file_name = 'D:\OneDrive - ITG Technologies\Documents\ITG Clients\Georgia-Pacific\FFT-S3 Data Processing\GP s3 facilities.txt'

with open(file_name, 'r') as f:
    data = f.readlines()

print(data[:3])
data2 = []

for key in data:
    if key.find('facility') != -1:
        data2.append(key)

data = data2
print(data[:3])
data2 = []

for key in data:
    start = key.find('facility')
    end = key.find('/')
    data2.append(key[start:end+1])

data = data2
print(data[:3])
data2 = ''

for key in data:
    data2 += f'--exclude "{key}*" '

data = data2
print(data[:])


with open(file_name[:-4]+'2'+file_name[-4:], 'w') as f:
    f.write(data)
