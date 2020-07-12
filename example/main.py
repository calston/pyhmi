from pyhmi import App


class Example(App):
    views = {
        'main': 'example/main.yaml'
    }

    def exit_click(self, button):
        self.stop()

if __name__ == '__main__':
    Example().run()
