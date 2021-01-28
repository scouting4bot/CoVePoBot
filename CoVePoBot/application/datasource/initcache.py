from CoVePoBot.application.datasource.mysql.connection import ExecuteQuerySelect

def init_vote_session_list(mysql):
    """ Initialize the vote_session_list. """

    # Select all vote sessions
    result = ExecuteQuerySelect('vote_session', {'columns2select':'*'}, mysql)
    vote_session_list = {}
    for row in result:
        vote_session_list[row[1]] = {"psw":row[2],"create_date":row[3]}
    print("initialization of cache: ====== Vote Sessions DONE")
    
    for vote_session_key in vote_session_list:

        # Select all otps for the 'vote_session_key'
        vote_session_list[vote_session_key]['otps'] = {}
        result = ExecuteQuerySelect('otp', {'columns2select':'*', 'vote_id':vote_session_key, 'status':'available'}, mysql)
        for row in result:
            vote_session_list[row[1]]['otps'][row[2]] = row[3]
        print("initialization of cache: ====== OTPs DONE")
    
        # Select all secrets for the 'vote_session_key'
        vote_session_list[vote_session_key]['secrets'] = {}
        result = ExecuteQuerySelect('secret', {'columns2select':'*', 'vote_id':vote_session_key, 'status':'enabled'}, mysql)
        for row in result:
            vote_session_list[row[1]]['secrets'][row[2]] = row[3]
        print("initialization of cache: ====== Secrets DONE")
    
    print("initialization of cache: ====== Full cache DONE")
    return vote_session_list