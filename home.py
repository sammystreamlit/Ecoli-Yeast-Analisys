import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title='Result Analysis', page_icon=":computer:",layout="wide")

intro = st.container()
dataset = st.container()
results = st.container()
inneranalysis = st.container()

with intro:
    st.title('Experiment Analysis')
    st.text('This analysis was acarried out by solving the bi-level problem on E.Coli and Yeast')
    st.text('The methods to solve each MN are -MILP- -Looping- -Callbacks-')
    st.text('The number of allowed knockouts are k=1,k=2,k=3')
    st.markdown("###### Some Characteristics of the MNs")
    st.markdown('- Met refers to the number of metabolites present in the MN')
    st.markdown('- Rxn refers to the number of reactions present in the MN')
    st.markdown('- The table shows the size of each metabolic network .')
    st.markdown("- The rxn number determines the number of continuous variables in the follower's problem and the number of binary variables in the master's problem.")


    met = [1805,1668,761,1655]
    rxn = [2583,2382,1075,2110]

    ms = ['iJO1366','iAF1260','iJR904','Y5.01']
    char = pd.DataFrame.from_dict({'Model':ms,'Met':met,'Rxn':rxn})
    st.write(char)
    st.write("The models used in this analysis are Y5.01,\n which corresponds to a yeast 'Saccharomyces cerevisiae' metabolic network. And, iJO1366, iAF1260, iJR904 describe a metabolic network for the E. Coli bacteria.")
    st.write("The bi-level objective for each E.Coli model is to max the succinate production. While, the bi-level objective in the yeast metabolic network is to max the ethanil production.")



with dataset:
    st.header('Data from Experiments')
    st.text('The data was collected and integrated in a dataframe for its easy analysis.')
    st.text("The column called Time_log is essentially the log base 10 of the computational time.")
    st.text('The Time_log makes it easier to scale and compare.')

    methods_data = pd.read_csv('MNData/All_methods_results_Ecoli.csv')
    st.subheader('Complete Data Frame - Ecoli')
    st.write(methods_data[['Model','Method','K','Time','Time_Log','Chem_OverP','Biomas_P']])
    fig1 = sns.catplot(x="Method",y="Time_Log",hue="K",aspect=3,data=methods_data)
    # st.pyplot(fig1)
    st.write("##")

    yeast_df = pd.read_csv('MNData/All_methods_results_Yeast.csv')
    st.subheader('Complete Data Frame - Yeast')
    st.write(yeast_df[['Model','Method','K','Time','Time_Log','Chem_OverP','Biomas_P']])
    fig2 = sns.catplot(x="Method",y="Time_Log",hue="K",aspect=3,data=yeast_df)
    # st.pyplot(fig2)
    st.write('##')
    st.write("The experiment when k=3, method = looping, model = Y5.01 had a traceback error on memmory issues and its values couldn't be estimated.")



    subdata = pd.DataFrame(methods_data.groupby(['K','Method']).describe())
    sub_yeast = pd.DataFrame(yeast_df.groupby(['K','Method']).describe())

    st.subheader("Data Groupby 'K' and 'Method'")
    st.text('These tables describes the data for Time_Log.')
    st.text('The resutls are grouped by k and method.')
    st.text('Each row reads as the time_log statistics for the three E.Coli MN given k and method.')
    st.text('The first table corresponds to E.Coli and the second table to Yeast.')
    st.write(subdata['Time_Log'])
    fig = sns.catplot(x="Method",y="Time_Log",hue="K",col='Model',aspect=.9,data=methods_data)
    st.pyplot(fig)
    st.write('##')

    st.write(sub_yeast['Time_Log'])
    fig1_yeast = sns.catplot(x="Method",y="Time_Log",hue="K",col='Model',aspect=3,data=yeast_df)
    st.pyplot(fig1_yeast)


with results:
    st.subheader('E.Coli Results')
    st.markdown('###### Time_log for each method under different k values.')
    st.pyplot(fig1)
    st.markdown('''- This graph clearly shows that method looping yields higher computational times than the other two methods.
    The next graph shows the computational time for each MN.''')
    st.markdown('###### Time_log for each MN and its solving methods')
    st.pyplot(fig)
    st.markdown('''- This graph further reveals looping as the slower method for the different k values.''')
    st.markdown('''- Moreover, the graph shows that for models iJR904 and iAF1260 the computing time using callbacks is faster than the other tow methods.''')
    st.markdown('''###### Chemicam Overproduction''')
    st.markdown('This graph shows the Succinate yields for each method and each k value fr the different MN')
    fig3 = sns.catplot(x="Method",y="Chem_OverP",hue="K",col='Model',aspect=.9,data=methods_data)
    st.pyplot(fig3)
    st.markdown('''Clearly models iJO1366 and iAF1260 show a more concise answers given the different methods, except for
    what couldd be considered an outlier in the callbacks method with k=3 and looping with k=1, respectively.
    Model iJR904 when solved by callbacks is currently yielding higher overproduction values for the different k values.
    The analysis is described in the feasibility analysis section.''')

with inneranalysis:
    st.subheader('Feasibility Analysis')
    st.markdown('''A possible way to asses the strategy provided by each method is to run experiments on the follower's model
    by inlcuding the strategy vector and calculate for the flux distribution in the entire metabolic network
    ''')
    st.markdown('### Models')
    st.markdown('##### Model 1')
    st.latex(r''' \max~ \nu_{biomas} \\
    st.~~ S*\nu =0 ; \\
        LB*\^{y} \leq \nu \leq UB*\^{y} ''')

    st.markdown('##### Model 2')
    st.latex(r''' \max~ \nu_{chemical} \\
    st.~~ S*\nu =0 ; \\
        LB*\^{y} \leq \nu \leq UB*\^{y} ''')
    st.write('##')
    st.markdown('###### Table Description ')
    st.markdown('''- The column 'Objective' in the table corresponds to the objective in Model 1 or Model 2''')
    st.markdown('''- Column 'Strategy' shows the reactions with value = 0 in the y vector''')
    st.markdown('''- V_Biomas and V_Chem is the corresponding value after each model was run.''')
    st.markdown('''- Values 2000, 1 in the V_Biomas and V_Chem columns respectively denote infeasibility in the follower's model given the proposed strategy''')

    st.subheader('iJR904 Analysis')
    ijr904 = pd.read_csv('MNData/Check_results_ijr904.csv',index_col=False)
    st.write(ijr904)
    dcittest = {'Model':['Callback','Callback','Model 1','Model 1','Model 2','Model 2'],'Rxn':['V_Biomas','V_Chem','V_Biomas','V_Chem','V_Biomas','V_Chem'],'Flux_Value':[0.1881,0.0628,0.1883,.08360,.1081,None]}
    newgr = pd.DataFrame.from_dict(dcittest)
    comp1 = sns.catplot(x="Flux_Value", y="Rxn", hue="Model", aspect=3,kind="swarm", data=newgr)
    st.pyplot(comp1)
    st.write('''The graph shows that the value for model 1 and the value that comes from the callback method for Biomas
    is virtually the same. Showing that the strategy keeps the biomas (growth) feasible. However the v_chem variates and the
    result that comes from the callback and the model 2 are close together.''')

    st.subheader('iJO1366 Analysis')
    ijo1366 = pd.read_csv('MNData/Check_results_ijo1366.csv',index_col=False)
    st.write(ijo1366)
    dicttest = {'Model':['Callback','Callback','Model 1','Model 1','Model 2','Model 2'],'Rxn':['V_Biomas','V_Chem','V_Biomas','V_Chem','V_Biomas','V_Chem'],'Flux_Value':[.1208,8.7676,.2388,.2490,.1208,8.7674]}
    newgr1 = pd.DataFrame.from_dict(dicttest)
    comp2 = sns.catplot(x="Flux_Value", y="Rxn", hue="Model", aspect=3,kind="swarm", data=newgr1)
    st.pyplot(comp2)
    st.write(''' The graph shows a similar V_Chem value for callback and model 2 and virtually the same values for model 1, model 2 and callback method.
    It also shows the strategy feasibility.''')


    st.subheader('iAF1260 Analysis')
    iaf1260 = pd.read_csv('MNData/Check_results_iaf1260.csv',index_col=False)
    st.write(iaf1260)
    dictiaf1260 = {'Model':['Looping','Looping','Model 1','Model 1','Model 2','Model 2'],'Rxn':['V_Biomas','V_Chem','V_Biomas','V_Chem','V_Biomas','V_Chem'],'Flux_Value':[.1881,.0628,.1881,.0628,.0941,None]}
    newgr2 = pd.DataFrame.from_dict(dictiaf1260)
    comp3 = sns.catplot(x="Flux_Value", y="Rxn", hue="Model", aspect=3,kind="swarm", data=newgr2)
    st.pyplot(comp3)
    st.write(''' The graph shows that model 1 and the method looping yield the same v_biomas and v-chemical values. Suggesting the strategy feasibility.''')

    st.subheader('Remarks')
    st.markdown('''- ###### Models iJO1366 and iAF1260 return the most consistent values for the different k values and different methods. ''')
    st.markdown('''- ###### It seems that looping and callback method values sometimes return a value from the follower's response when max chemical and max biomas.''')
