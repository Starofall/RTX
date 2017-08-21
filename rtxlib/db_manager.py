import sqlite3
import json

def create_connection(db_file = '../../../../../SavedExperiments.db'):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None
def insert_into_experiments(db,
                            result_folder ,
                            sample_size_method,
                            definition_file_path):
    conn = create_connection(db)

    conn.execute("INSERT INTO experiments (results_path,sample_size_method,definition_file_path) \
          VALUES ('"+ result_folder+ "','"+ sample_size_method+"','"+ definition_file_path+"' )");
    conn.commit()
    print( "Records created successfully");
    conn.close()

def insert_into_results(db,
                        results_path,
                        metric,
                        total_sample_size,
                        total_x2 ,
                        total_x ):

    conn = create_connection(db)

    conn.execute("INSERT INTO results (results_path,metric,total_sample_size, total_x2, total_x) \
          VALUES ('"+ results_path+ "','"+ metric+"','"+ str(total_sample_size)+"','" + str(total_x2)+ "','" + str(total_x)+ "' )");
    conn.commit()
    print( "Records created successfully");
    conn.close()

def insert_into_config(db,
                       path,
                       experiment_id,
                       execution_strategy,
                       change_provider
                       ):

    conn = create_connection(db)

    conn.execute("INSERT INTO config (path,experiment_id,execution_strategy, change_provider) \
          VALUES ('"+ path+ "','"+ str(experiment_id) +"','"+ execution_strategy+"','"+ change_provider+ "' )");
    conn.commit()
    print( "Records created successfully");
    conn.close()

def save_experiment(wf, db_name):
    print( "Inserting Experiment into DB")
    insert_into_experiments(db_name, "saved_experiment/" , wf.execution_strategy["sample_size_method"], wf.folder)

def save_config(wf, db_name):
    print( "Inserting Config into DB")
    conn = create_connection(db_name)

    a = conn.execute("SELECT experiment_id FROM experiments WHERE definition_file_path = '" + wf.folder +"'");
    exp_id = 0
    for x in a:
        exp_id = x
    conn.close()
    print("exp_id = " , exp_id)
    insert_into_config(db_name, wf.folder, exp_id, json.dumps(wf.execution_strategy), json.dumps(wf.change_provider))

def save_result(wf, db_name, total_sample_size , total_x2, total_x):
    print( "Inserting results into DB")
    ## TODO: query the same type of experiment and addupp the counts
    insert_into_config(db_name, wf.folder, 'overhead', total_sample_size, total_x2, total_x)




