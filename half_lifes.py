import streamlit as st
import pandas as pd
pd.set_option('display.precision', 2)
df = pd.read_csv('data/nuclides.csv')
#df = pd.read_csv("https://nds.iaea.org/relnsd/v0/data?"+"fields=ground_states&nuclides=all")

st.session_state.sel = st.radio('age range', ['a', 'ka', 'Ma', 'Ga'], index=3, horizontal=True)

col1, col2, col3 = st.columns([1,1,3])
with col1:
    st.session_state.min = st.number_input('min', value = .1)
with col2:
    st.session_state.max = st.number_input('max', value = 100)
with col3:
    pass

sec_in_year = 31556952
df3 = df[['symbol','decay_1','decay_1_%']]
df3.insert(0, 'mass number', df['z'] + df['n'])
df3.insert(2, 'half life (years)', pd.to_numeric(df['half_life_sec'], errors='coerce') / sec_in_year)


if st.session_state.sel == 'a':
    scale = 1
elif st.session_state.sel == 'ka':
    scale = 10**3
elif st.session_state.sel == 'Ma':
    scale = 10**6
elif st.session_state.sel == 'Ga':
    scale = 10**9

fil = (df3['half life (years)'] >= st.session_state.min * scale) & (df3['half life (years)'] <= st.session_state.max * scale)
df4 = df3[fil]
df4.insert(2, 'half life ('+str(st.session_state.sel)+')', df3[fil]['half life (years)'] / scale)

st.dataframe(df4.drop(columns=['half life (years)']))