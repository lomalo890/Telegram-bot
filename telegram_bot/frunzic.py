def data(integer):
    try:
        with open('secret_datas.txt', 'r') as file:
            lines = file.readlines()
        return lines[integer]
    except Exception as e:
        print(e)