class Snake:
    def __init__(self, id, health, body_list):
        self.id = id
        self.health = health
        self.body_list = body_list

    def head(self):
        return self.body_list[0]

    def tail(self):
        return self.body_list[len(self.body_list) - 1]

    def neck(self):
        return self.body_list[1]

    def prev_head(self):
        if len(self.body_list) > 1:
            return self.body_list[1]
        else:
            return 0

    def length(self):
        return len(self.body_list)

    def curr_dir(self):
        if self.length() > 1:
            return dir(self.neck(), self.head())
        else:
            print("Error, snake length not larger than 1.")
            return -1
