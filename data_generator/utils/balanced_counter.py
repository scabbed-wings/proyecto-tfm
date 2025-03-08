class Balanced_Counter:
    def __init__(self, target_count) -> None:
        self.target_count = target_count
        self.count_atribute_relations = 0 if self.target_count is not None else None
        self.count_entity_relations = 0 if self.target_count is not None else None

    def count_or_not(self) -> bool:
        if self.target_count is None:
            return False
        return True

    def count_atribute_is_finished(self) -> bool:
        if self.count_or_not():
            if self.count_atribute_relations == self.target_count:
                return True
        return False

    def count_entity_relation_is_finished(self) -> bool:
        if self.count_or_not():
            if self.count_entity_relations == self.target_count:
                return True
        return False

    def is_finished(self) -> bool:
        if self.count_atribute_is_finished() and self.count_entity_relation_is_finished():
            return True
        return False

    def add_count_atribute(self) -> None:
        self.count_atribute_relations += 1

    def add_count_entity_relation(self) -> None:
        self.count_entity_relations += 1

    def print_counter(self) -> None:
        print(f"Target number = {self.target_count}\t Number atributes relations = {self.count_atribute_relations}\t \
              Number of entity-relation = {self.count_entity_relations}")
