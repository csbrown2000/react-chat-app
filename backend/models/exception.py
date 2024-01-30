# Exception model


class EntityNotFoundException(Exception):
	"""
	Exception raised when an entity is not found in the database.

	Attributes:
		entity_name (str): The name of the entity.
		entity_id (str): The ID of the entity.
	"""

	def __init__(self, *, entity_name: str, entity_id: str):
		self.entity_name = entity_name
		self.entity_id = entity_id



