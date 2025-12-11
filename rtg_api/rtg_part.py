from __future__ import annotations
from .requirements import Vector3, VirtualInstance, AttachmentType, List, base64, json
from .rtg_object import RtgObject

class RtgPart:
    @staticmethod
    def get_ball_id(object_name: str, direction: Vector3):
        return RtgObject.get_attachment_id(object_name, "ball", direction)
    
    @staticmethod
    def get_cup_id(object_name: str, direction: Vector3):
        return RtgObject.get_attachment_id(object_name, "cup", direction)

    def __init__(self, object_name: str):
        object = RtgObject(object_name)

        self.properties = {}
        self.structure = None

        self._attachments_classes = []
        self._object = object
        self._name = object_name

    def get_ball_from_location(self, location: Vector3):
        return RtgPart._Attach.get_or_create(self, self._object.get_closest_ball(location), "ball")
    
    def get_cup_from_location(self, location: Vector3):
        return RtgPart._Attach.get_or_create(self, self._object.get_closest_cup(location), "cup")
    
    def get_attachment(self, location: Vector3):
        return RtgPart._Attach.get_or_create(self, self._object.get_closest_attachment(location))

    def get_attachment_from_id(self, id: int):
        for attachment in self._object.attachments:
            if attachment.find_first_child("Id").get_property("Value") != id:
                continue
            return RtgPart._Attach.get_or_create(self, attachment)

    def clone(self):
        cloned_part = RtgPart(self._name)
        cloned_part.properties = self.properties.copy()

        return cloned_part

    def set_property(self, name: str, value: any):
        self.properties[name] = value

    class _Attach:
        def __init__(self, outer: RtgPart, attachment: VirtualInstance, type: AttachmentType):
            self._outer = outer
            self._attachment = attachment
            
            self._type = type
            self._end = None
            self.id = int(attachment.find_first_child("Id").get_property("Value"))
            
            outer._attachments_classes.append([attachment, self])

        @classmethod
        def get_or_create(cls, outer: RtgPart, attachment: VirtualInstance, type: AttachmentType = None):
            for att, instance in outer._attachments_classes:
                if att is attachment:
                    return instance
            
            if type == None:
                type = "ball" if attachment.get_property("Name") == "BallAttachment" else 'cup'

            return cls(outer, attachment, type)
        
        @classmethod
        def exists(cls, outer: RtgPart, attachment: VirtualInstance):
            for att, instance in outer._attachments_classes:
                if att is attachment:
                    return instance
            
            return None
        
        def attach(self, end: RtgPart._Attach):
            assert self._end == None, "Cannot attach when already attached !"
            assert self._type != end._type, f"Cannot attach a {self._type} to itself !"

            self._end = end
            end._end = self

            if self._outer.structure:
                self._outer.structure._version += 1
            if end._outer.structure:
                end._outer.structure._version += 1

class Structure:
    def __init__(self):
        self.parts: List[RtgPart] = []
        self._version = 0

        self._last_code = None
        self._last_code_version = -1
    
    def add(self, part: RtgPart):
        if part in self.parts:
            return
        assert part.structure == None, f"{part._name} is already member of a structure"

        self.parts.append(part)
        self._version += 1
        part.structure = self

    def get_all_parts(self):
        current_parts: List[RtgPart] = []
        waiting_parts = []

        def traverse(part: RtgPart):
            if part in current_parts:
                return

            current_parts.append(part)
            for attachment in part._object.attachments:
                attach: RtgPart._Attach = part._Attach.exists(part, attachment)
                if not attach:
                    continue
                if not attach._end:
                    continue

                waiting_parts.append(attach._end._outer)

        for part in self.parts:
            traverse(part)
        
        while len(waiting_parts) > 0:
            traverse(waiting_parts.pop())
        
        return current_parts

    def compile(self):
        current_parts = self.get_all_parts()
        transformed_list: List[List[RtgPart, int, List[str, list, list]]] = []

        for part in current_parts:
            transformed_list.append([part, len(transformed_list) + 1, [
                part._name,
                [],
                part.properties
            ]])
        
        def find_part_id(part: RtgPart):
            for target in transformed_list:
                if target[0] != part:
                    continue

                return target[1]
        
        for final in transformed_list:
            part = final[0]
            balls = part._object.ball_attachments

            for ball in balls:
                connection = []
                attach: RtgPart._Attach = part._Attach.exists(part, ball)
                if not attach:
                    continue
                if not attach._end:
                    continue

                connection.append(attach.id)
                connection.append(attach._end.id)
                connection.append(find_part_id(attach._end._outer))
                final[2][1].append(connection)

        encoded_ready_list = []
        for final in transformed_list:
            encoded_ready_list.append(final[2])

        return base64.b64encode(json.dumps(encoded_ready_list).encode()).decode()
    
    @property
    def code(self):
        if self._last_code_version != self._version:
            self._last_code = self.compile()
        
        return self._last_code