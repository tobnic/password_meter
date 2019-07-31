import sys, select, json
import lib_higher_strucutre as lib_hs
import lib_adaptive_memory as lib_am
import lib_trivial_pwd as lib_triv
import lib_brute_force as lib_bf
from ConfigParser import SafeConfigParser


PATH = "PSE/"
#PATH = ""
if __name__ == '__main__':
    

    arg_len = len(sys.argv)
    
    #
    # HIGHER STRUCTURE, ADAPTIVE MEMORY
    #
    
    hs_score = 0
    am_score = 0
    pwb_score = 0
    bf_score = 0
    
    hs_extra_words = []
    am_extra_words = []
    triv_extra_words = []
    
    loadStandardConfig = False
    
    #
    # READ CUSTOM CONFIG FILES
    #
    if arg_len > 2:
        
        session_id = single_pwd = sys.argv[2]
        
    
        try:
            config = SafeConfigParser()
            config.read('./'+PATH+'user_config/config_'+str(session_id)+'.ini')
            
            #trivlia
            hs_score_level = float(config.get('pm_config','scoreLevelHS').replace("\"", ""))
            am_score_level = float(config.get('pm_config','scoreLevelAM').replace("\"", ""))
            
            #non trivial
            pwb_score_level = float(config.get('pm_config','scoreLevelDic').replace("\"", ""))
            bf_score_level = float(config.get('pm_config','scoreLevelBF').replace("\"", ""))
        
            # score normalization hampel tanh
            score_normalization_ugh = float(config.get('pm_config','ugh').replace("\"", ""))
            score_normalization_ogh = float(config.get('pm_config','ogh').replace("\"", ""))
            
            # score strength bf heuristic
            bfn_score_strength = float(config.get('pm_config','scoreStrengthBFN').replace("\"", ""))
            bfnogmax_score_strength = float(config.get('pm_config','scoreStrengthBFNOGMAX').replace("\"", ""))
            bftmax_score_strength = float(config.get('pm_config','scoreStrengthBFTMAX').replace("\"", ""))
            
            #adaptive memory max length
            ammax_score_strength = float(config.get('pm_config','scoreStrengthAMMAX').replace("\"", ""))
        except:
            print "error"
            loadStandardConfig = True
    
        try:
            am_extra_words += open('./'+PATH+'user_config/user_data_adaptive_'+str(session_id)+'.txt').read().split()
        except:
            print "User HS File Not Found"

        try:
            triv_extra_words += open('./'+PATH+'user_config/user_data_trivial_'+str(session_id)+'.txt').read().split()
        except:
            print "User Trivial File Not Found"
            
        try:
            hs_extra_words += open('./'+PATH+'user_config/user_data_higherstruct_'+str(session_id)+'.txt').read().split()
        except:
            print "User AM File Not Found"

    # Set standard parameter
    else:
        loadStandardConfig = True


    #
    # STANDARD CONFIG
    #
    if loadStandardConfig:
        print "Standard Config loaded"
        #trivlia
        hs_score_level = 0.2
        am_score_level = 0.2
        
        #non trivial
        pwb_score_level = 0.3
        bf_score_level = 0.3

        # score normalization hampel tanh
        score_normalization_ugh = 180
        score_normalization_ogh = float(3)/2
        
        # score strength bf heuristic
        bfn_score_strength = 94
        bfnogmax_score_strength = 100000000
        bftmax_score_strength = 32140800
        
        #adaptive memory max length
        ammax_score_strength = 4
    
    
    # lib
    hs_main = lib_hs.higher_structure()
    am_main = lib_am.adaptive_memory()
    triv_main = lib_triv.trivial_pwd()
    bf_main = lib_bf.brute_force()


    # train higher structe model
    words = open('./'+PATH+'training_data_higherstruct.txt').read().split()
    words += hs_extra_words
    hs_main.trainModelWith(score_normalization_ugh,score_normalization_ogh,words)
    
    # conf/train adaptive memory model
    words = open('./'+PATH+'training_data_adaptive.txt').read().split()
    words += am_extra_words
    am_main.trainModelWith(ammax_score_strength,score_normalization_ugh,score_normalization_ogh, words)
    
    # train trivial model
    words = open('./'+PATH+'training_data_trivial_pwds.txt').read().split()
    words += triv_extra_words
    triv_main.trainModelWith(words)
    
    # train / conf Brute Force model
    bf_main.trainModelWith(bfn_score_strength,bfnogmax_score_strength,bftmax_score_strength)
    
    # calc score for passwords from stdin
    if select.select([sys.stdin,],[],[],0.0)[0]:
        for single_pwd in sys.stdin:
            hs_score = hs_main.score_from_PW(single_pwd)
            am_score = am_main.score_from_PW(single_pwd)
            pwb_score = triv_main.score_from_PW(single_pwd)
            bf_score = bf_main.score_from_PW(single_pwd)


            #Final Score Calculation
            final_score = 0
            final_score += am_score * am_score_level
            final_score += hs_score * hs_score_level
            final_score += pwb_score * pwb_score_level
            final_score += bf_score * bf_score_level

            print "\n+++++++++++++++++++++++++++"
            print "FINAL SCORE: %.2f" %final_score
            print "+++++++++++++++++++++++++++"

    # calc score for passwords from args

    if arg_len > 1:
        #password for scoring
        single_pwd = sys.argv[1].lower()
        
        # calc score for passwords from args
        hs_score = hs_main.score_from_PW(single_pwd)
        am_score = am_main.score_from_PW(single_pwd)
        pwb_score = triv_main.score_from_PW(single_pwd)
        bf_score = bf_main.score_from_PW(single_pwd)
        
        
        #Final Score Calculation
        final_score = 0
        final_score += am_score * am_score_level
        final_score += hs_score * hs_score_level
        final_score += pwb_score * pwb_score_level
        final_score += bf_score * bf_score_level
        
        print "\n+++++++++++++++++++++++++++"
        print "FINAL SCORE: %.2f" %final_score
        print "+++++++++++++++++++++++++++"
    # Generate some data to send to PHP
    final_score *= pwb_score/10
    final_score *= bf_score/10
    result = {'final_score': final_score,'hs_score': hs_score,'am_score': am_score,'pwb_score': pwb_score,'bf_score': bf_score}

    # Send it to stdout (to PHP)
    print json.dumps(result)
