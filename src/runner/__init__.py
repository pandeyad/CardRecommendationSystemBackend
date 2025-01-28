class RunnerFactory:
    _instance = None  # Private class variable to store the single instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # If no instance exists, create one
            cls._instance = super(RunnerFactory, cls).__new__(cls, *args, **kwargs)
            cls._instance.runner_registry = []  # Initialize the registry
        return cls._instance  # Return the existing instance

    def register(self, cls):
        """
        Registers a class to the runner registry, but first checks if it implements `run()` and its return type.
        """
        if not isinstance(cls, type):
            raise TypeError(f"Expected a class, but got {type(cls)}")

        # Ensure the class implements the `run()` method
        if "run" not in dir(cls):
            raise AttributeError(f"The class {cls.__name__} does not implement the `run()` method.")

        # Check that `run()` does not return anything (i.e., must return None)
        if not self._is_run_method_valid(cls):
            raise ValueError(f"The `run()` method in class {cls.__name__} must not return anything.")

        # Ensure the class is callable (i.e., can be instantiated)
        if not callable(cls):
            raise TypeError(f"The class {cls.__name__} is not callable and cannot be instantiated.")

        # Add the class to the registry if it passes validation
        self.runner_registry.append(cls)
        print(f'Registered class : {cls.__name__}')
        return cls

    def _is_run_method_valid(self, cls):
        """
        Check if the `run()` method of the class does not return anything (i.e., returns None).
        """
        # Check if the `run()` method is a function and its return type is None
        run_method = getattr(cls, "run")
        if run_method.__code__.co_flags & 0x4:  # Check if the function has a return statement
            if run_method() is not None:
                return False
        return True

    def get_all_runners(self):
        """
        Returns a list of all registered runners (extractors).
        """
        return self.runner_registry

    def run_all(self):
        """
        Run all registered runners.
        Calls the `run()` method of each registered runner.
        """
        for runner in self.runner_registry:
            runner().run()  # Assuming `run()` method exists in each registered class


# Expose the singleton instance globally
runner_factory = RunnerFactory()




