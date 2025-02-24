from abc import ABC, abstractmethod
import os

class IFileStorage(ABC):
    """Interface for file storage implementations."""

    @abstractmethod
    def save(self, name: str, location: str, data: str) -> None:
        """Saves a file with the given name, location, and data."""
        pass


class LocalFileStorage(IFileStorage):
    """Concrete implementation of IFileStorage for local file system."""

    def save(self, name: str, location: str, data: str) -> None:
        """Saves data to a local file."""
        os.makedirs(location, exist_ok=True)  # Ensures the directory exists
        file_path = os.path.join(location, name)

        try:
            with open(file_path, "w") as f:
                f.write(data)
            print(f"File saved successfully: {file_path}")
        except OSError as e:
            print(f"Error saving file: {e}")


class XrayTestRunnerFile:
    """High-level class that uses a storage implementation to save files."""

    def __init__(self, storage: IFileStorage) -> None:
        self.storage = storage  # Injected dependency

    def save(self, name: str, location: str, data: str) -> None:
        """Delegates saving logic to the storage implementation."""
        self.storage.save(name, location, data)
