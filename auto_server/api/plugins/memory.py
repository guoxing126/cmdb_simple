from repository import models

class Memory(object):
    def __init__(self,server_obj,info):
        self.server_obj=server_obj
        self.memory_dict=info

    def process(self):
        new_memory_info_dict=self.memory_dict['data']
        old_memory_info_list=self.server_obj.memory.all()

        new_memory_slot_set=set(new_memory_info_dict.keys())
        old_memory_slot_set={obj.slot for obj in old_memory_info_list}

        add_slot_list=new_memory_slot_set.difference(old_memory_slot_set)
        del_slot_list=old_memory_slot_set.difference(new_memory_slot_set)
        update_slot_list=new_memory_slot_set.intersection(old_memory_slot_set)

        add_record_list=[]

        for slot in add_slot_list:
            value=new_memory_info_dict[slot]
            tmp="添加内存"
            add_record_list.append(tmp)
            value['server_obj']=self.server_obj
            models.Memory.objects.create(**value)

        models.Memory.objects.filter(server_obj=self.server_obj,slot__in=del_slot_list).delete()

        for slot in update_slot_list:
            value=new_memory_info_dict[slot]
            print(value)
            obj=models.Memory.objects.filter(server_obj=self.server_obj,slot=slot).first()
            for k,new_val in value.items():
                old_val=getattr(obj,k)
                if old_val != new_val:
                    setattr(obj,k,new_val)
            obj.save()