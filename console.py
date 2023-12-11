#!/usr/bin/python3
"""
Simple dashboard cmd
"""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def test(string: str):
    print(type(string))
    string = string.split(" ")
    print(string[-1].replace('"', ""))


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def do_quit(self, arg):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program"""
        print("")
        return True

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        Ex: $ create BaseModel
        """
        if arg:
            try:
                print(HBNBCommand.__classes[arg]().id)
                storage.save()
                storage.reload()
            except KeyError:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        Ex: $ show BaseModel 1234-1234-1234
        """
        argv = arg.split(" ")
        if not arg:
            print("** class name missing **")
        elif len(argv) == 1:
            print("** class doesn't exist **") if (
                argv[-1] not in HBNBCommand.__classes.keys()
            ) else (print("** instance id missing **"))
        elif len(argv) == 2:
            objs = storage.all()
            key = argv[0] + "." + argv[1]
            try:
                print(objs[key])
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance
        based on the class name and id (save the change into the JSON file)
        Ex: $ destroy BaseModel 1234-1234-1234
        """
        argv = arg.split(" ")
        if not arg:
            print("** class name missing **")
        elif len(argv) == 1:
            print("** class doesn't exist **") if (
                argv[-1] not in HBNBCommand.__classes.keys()
            ) else (print("** instance id missing **"))
        elif len(argv) == 2:
            objs = storage.all()
            key = argv[0] + "." + argv[1]
            try:
                del objs[key]
                storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name
        Ex: $ all BaseModel or $ all
        """
        objs = storage.all()
        objs_list = []
        if not arg:
            for value in objs.values():
                objs_list.append(str(value))
        else:
            if arg in HBNBCommand.__classes.keys():
                for key in objs.keys():
                    if re.match(f"{arg}\\..+", key):
                        objs_list.append(str(objs[key]))
            else:
                print("** class doesn't exist **")
        if len(objs_list) != 0:
            print(objs_list)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file)
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        if not arg:
            print("** class name missing **")
            return False
        argv = arg.split(" ")
        objs = storage.all()
        obj = {}
        if argv[0] not in HBNBCommand.__classes.keys():
            print("** class doesn't exist **")
            return False
        if len(argv) < 2:
            print("** instance id missing **")
            return False
        key = argv[0] + "." + argv[1]
        try:
            obj = objs[key]
        except KeyError:
            print("** no instance found **")
            return False
        if len(argv) < 3:
            print("** attribute name missing **")
            return False
        if len(argv) < 4:
            print("** value missing **")
            return False
        argv[3] = argv[3].replace('"', "")
        if type(obj.__dict__[argv[2]]) is int:
            obj.__dict__[argv[2]] = int(argv[3])
        elif type(obj.__dict__[argv[2]]) is float:
            obj.__dict__[argv[2]] = float(argv[3])
        else:
            obj.__dict__[argv[2]] = argv[3]
        storage.save()
        storage.reload()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
