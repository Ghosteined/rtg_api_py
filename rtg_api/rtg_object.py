from .requirements import List, VirtualInstance, Vector3, CFrame, AttachmentType, root

class RtgObject:
    @staticmethod
    def get_closest_attachment(attachments: List[VirtualInstance], direction: Vector3) -> VirtualInstance:
        attachment_differences = []
        
        for attachment in attachments:
            attachment_cframe: CFrame = attachment.get_property("CFrame")
            attachment_position = attachment_cframe.position

            diff_x = abs(attachment_position.x - direction.x)
            diff_y = abs(attachment_position.y - direction.y)
            diff_z = abs(attachment_position.z - direction.z)
            diff_total = diff_x + diff_y + diff_z

            attachment_differences.append([attachment, diff_total])
        attachment_differences.sort(key=lambda x: x[1])

        return attachment_differences[0][0]

    @staticmethod
    def get_attachment_id(object_name: str, type: AttachmentType, direction: Vector3):
        object = root.find_first_child(object_name)
        assert object != None, f"Object '{object_name}' not found !"

        attachment_name = "CupAttachment" if type == "cup" else "BallAttachment"
        targets = []
        for child in object.get_descendants():
            if child.class_name != "Attachment":
                continue

            name = child.get_property("Name")
            if name == attachment_name:
                targets.append(child)
        
        return RtgObject.get_closest_attachment(targets, direction).find_first_child("Id").get_property("Value")

    def __init__(self, object_name: str):
        object = root.find_first_child(object_name)
        assert object != None, f"Object '{object_name}' not found !"
        
        attachments: List[VirtualInstance] = []
        cup_attachments: List[VirtualInstance] = []
        ball_attachments: List[VirtualInstance] = []
        for child in object.get_descendants():
            if child.class_name != "Attachment":
                continue
            
            name = child.get_property("Name")
            if name == "CupAttachment":
                cup_attachments.append(child)
            elif name == "BallAttachment":
                ball_attachments.append(child)
            else:
                continue
            attachments.append(child)
        
        self.model = object
        self.attachments = attachments
        self.cup_attachments = cup_attachments
        self.ball_attachments = ball_attachments

    def get_closest_ball(self, unit: Vector3) -> VirtualInstance:
        return RtgObject.get_closest_attachment(self.ball_attachments, unit)

    def get_closest_cup(self, unit: Vector3) -> VirtualInstance:
        return RtgObject.get_closest_attachment(self.cup_attachments, unit)