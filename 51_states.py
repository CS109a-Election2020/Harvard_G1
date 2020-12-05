df = big_df
correlation_matrix = abs(int(cor_mat*10))


for state in states:  # state = Alabama
    df = []
    # state is the considered state
    for state_2 in states.remove(state):  # state_2 = ALaska
        data_state_2 = df['state' == state_2]
        value_cor = correlation_matrix[state][state_2]
        df.append(value_cor*data_state_2)
        # modelling phase
        # interesting part: are our models in line with the swing states ? this will interesting for the report
        # some kind of CI according to the states: swing vs non-swing
