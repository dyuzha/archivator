from neotui import App


if __name__ == '__main__':
    app = App()
    app.run()

    if app.build == True: 
        app.build_dir()
