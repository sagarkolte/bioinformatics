import src.data_prep as dp

target_id = 'CHEMBL3927'
standard_type = 'IC50'
print(dp.main_pipe(target_id,standard_type))