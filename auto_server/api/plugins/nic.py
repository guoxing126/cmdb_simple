from repository import models

class Nic(object):
    def __init__(self,server_obj,info):
        self.server_obj = server_obj
        self.nic_dict = info

    def process(self):
        new_disk_info_dict = self.nic_dict['data']
        old_disk_info_list = self.server_obj.nic.all()

        new_nic_set=set(new_disk_info_dict.keys())
        old_nic_set={obj.name for obj in old_disk_info_list}

        add_slot_list=new_nic_set.difference(old_nic_set)
        del_slot_list=old_nic_set.difference(new_nic_set)
        update_slot_list=new_nic_set.intersection(old_nic_set)

        add_record_list=[]

        for nic in add_slot_list:
            value=new_disk_info_dict[nic]
            tmp="添加网卡……"
            add_record_list.append(tmp)
            value['name']=nic
            value['server_obj']=self.server_obj
            models.NIC.objects.create(**value)

        models.NIC.objects.filter(server_obj=self.server_obj,name__in=del_slot_list).delete()

        for nic in update_slot_list:
            value=new_disk_info_dict[nic]
            obj=models.NIC.objects.filter(server_obj=self.server_obj,name=nic).first()
            for k,new_val in value.items():
                old_val=getattr(obj,k)
                if old_val!=new_val:
                    setattr(obj,k,new_val)
            obj.save()
