#method oveerriding

class animal:
    def sound(self):
        print("animal make sound")
class dog(animal):
    def sound(self):
        print("Dog barks")
d= dog()
d.sound()
        