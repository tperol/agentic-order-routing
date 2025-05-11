from setuptools import setup, find_packages

setup(
    name="agentic-order-routing",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "openai-agents",
        "python-dotenv",
    ],
    python_requires=">=3.12",
) 