import os
import subprocess
import sys

from setuptools import setup, find_packages, Command
import glob

def parse_requirements(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found.")
    with open(filename, "r") as file:
        return [line.split("#")[0].strip() for line in file.read().splitlines()]  # Remove comments


class CleanAndRebuildCommand(Command):
    description = "Clean old build files, rebuild the package, and install the fresh version"
    user_options = []  # No options needed for this command

    def initialize_options(self):
        # No options to initialize
        pass

    def finalize_options(self):
        # No finalization needed
        pass

    def run(self):
        try:
            # Step 1: Clean up old build files
            print("Cleaning up old build artifacts...")
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "CardRecommendationModel", "-y"], check=False)

            if os.path.exists('build'):
                subprocess.run(['rm', '-rf', 'build'], check=True)
            if os.path.exists('dist'):
                subprocess.run(['rm', '-rf', 'dist'], check=True)
            if os.path.exists('*.egg-info'):
                subprocess.run(['rm', '-rf', '*.egg-info'], check=True)

            # Step 2: Rebuild the package
            print("Rebuilding the package...")
            subprocess.run([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'], check=True)

            # Step 3: Find the .whl file in the dist directory
            wheel_files = glob.glob('dist/*.whl')  # Glob to find the .whl files in the dist directory
            if not wheel_files:
                raise FileNotFoundError("No .whl file found in the dist/ directory")

            # Install the newly built package
            print(f"Installing the newly built package from {wheel_files[0]}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', wheel_files[0]], check=True)

            print("Clean, rebuild, and install completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)


setup(
    name="CardRecommendationModel",  # Replace with your project name
    version="0.1.0",    # Replace with your project version
    author="Aditya Pandey",  # Replace with your name
    author_email="pandeyad22@gmail.com",  # Replace with your email
    description="Simple RAG application for recommending credit cards based on scheduled crawled data for various bank",  # Project description
    long_description=open("README.md").read(),  # Long description from README
    long_description_content_type="text/markdown",  # Type of README file
    url="",  # Replace with your project URL
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=parse_requirements("requirements.txt"),
    data_files=[
        ('./configurations', glob.glob('configurations/*.yaml') + glob.glob('configurations/*.yml')),
    ],  # Include YAML files in 'configurations'
    include_package_data=True,      # Ensure non-Python files are included
    cmdclass={
        'rebuild': CleanAndRebuildCommand,  # Register the custom command
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "crm=src.app:main",  # Entry point for the Flask app
        ],
    },
    python_requires=">=3.9",  # Minimum Python version
)
