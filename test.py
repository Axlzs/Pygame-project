# Define an outside function
def external_function():
    print("This function is outside the class!")

class MyClass:
    def __init__(self):
        print("MyClass instance created.")

    def call_external_function(self):
        # Call the external function inside the class
        external_function()

# Create an instance of MyClass
my_instance = MyClass()
my_instance.call_external_function()
