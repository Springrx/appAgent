from and_controller import list_all_devices, AndroidController, traverse_tree

clickable_list = []
traverse_tree('../apps/didi/demos/self_explore_2024-01-08_19-58-40/7.xml', clickable_list, "clickable", True)
print(clickable_list)