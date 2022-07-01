import streamlit as st
import pandas as pd

st.write('# RD / RT Phone Triage')

with st.form('triage'):
    eye = st.radio(
        'Which eye has symptoms?',
        options=['One eye', 'Both eyes'],
    )
    timing = st.radio(
        'When did your symptoms start?',
        ['Within 24 hours', 'Between 24 hours and 72 hours ago', 'More than 72 hours ago'],
    )
    curtain = st.radio(
        label='Have you experienced either a non-moving curtain or veil over your vision?',
        options=[True, False],
        format_func=lambda x: 'Yes' if x else 'No',
        index=1,
    )
    blur = st.radio(
        'Ignoring your floater(s), have you experienced blurred vision? If so, how would you characterize it?',
        ['None', 'Intermittent', 'Constant']
    )

    myopia = st.radio(
        label='When you were a young adult (before any procedures to your affected eye), did you need glasses to see to drive?',
        options=[True, False],
        format_func=lambda x: 'Yes' if x else 'No',
        index=1,
    )
    history = st.radio(
        label='Have you had a prior retinal tear or detachment in either eye?',
        options=[True, False],
        format_func=lambda x: 'Yes' if x else 'No',
        index=1,
    )
    diabetes = st.radio(
        label='Are you diabetic?',
        options=[True, False],
        format_func=lambda x: 'Yes' if x else 'No',
        index=1,
    )
    surgery = st.radio(
        label='Have you ever gone to the operating room for retinal surgery in either eye?',
        options=[True, False],
        format_func=lambda x: 'Yes' if x else 'No',
        index=1,

    )

    # Every form must have a submit button.
    submitted = st.form_submit_button('Submit')
    if submitted:
        ## --- Calculate risk score --- ##
        points = {}

        points['eye'] = 5 if eye == 'One eye' else 1
        points['surgery'] = 10 if surgery else 1
        points['myopia'] = 3 if myopia else 1
        points['history'] = 10 if history else 1
        points['diabetes'] = 1 if diabetes else 5
        points['surgery'] = 10 if surgery else 1

        if timing == 'Within 24 hours':
            points['timing'] = 6
        elif timing == 'Between 24 hours and 72 hours ago':
            points['timing'] = 3
        else:
            points['timing = 1']

        if curtain or blur == 'Constant':
            points['curtain/blur'] = 14
        else:
            points['curtain/blur'] = 1

        total = sum(points.values())
        st.write(f'### Risk Score: {total}')
        st.write('### Recommendation: ***')
        st.markdown('*For testing, let\'s see the score breakdown*')
        st.write(points)


df = pd.DataFrame({
    'Cutoff Score':[17, 20, 23, 26, 29, 32, 35, 38, 41, 44],
    'Percent -RT/RD Included':['64.80%', '53.07%', '46.37%', '35.75%', '27.37%', '16.20%', '8.94%', '5.59%', '3.91%', '1.12%'],
    'Percent +RT/RD Included': ['100.00%', '100.00%', '92.86%', '92.86%', '92.86%', '85.71%', '64.29%', '57.14%', '35.71%', '35.71%']
})
st.table(df)