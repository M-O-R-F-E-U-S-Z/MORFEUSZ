import data_manager

CLASSES = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']

if __name__ == '__main__':
    data_manager.create_data()
    X, Y = data_manager.load_data()