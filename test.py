import criterion as cr
var = cr.capture("Enter 1 for  inspect, Enter 2 for repair, 3 for both inspect and repair")
cr.collect_data("safety.xlsx", "tasks.xlsx", var)


all_criteria= [cr.first_criteria, cr.second_criteria,cr.third_criteria,cr.fourth_criteria,cr.fifth_criteria,cr.sixth_criteria]
for criteria in all_criteria:
    print("   ")
    criteria(cr.actions_dict)
    print("APPLYING CRITERIA: ", criteria.__name__)
    print(cr.result)
result1, result2 = cr.result_sorting(cr.result, var)


 

