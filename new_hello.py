import streamlit as st

st.graphviz_chart('''
digraph G {
        graph [
            nodesep=0.5;
            rankdir="LR";
            cencentrate=true;
            splines="spline";
            fontname="Helvetica";
            pad="0.2,0.2",
            label="",

        ];

        node [shape=plain, fontname="Helvetica"];
        edge [
            dir=both,
            fontsize=12,
            arrowsize=0.9,
            penwidth=1.0,
            labelangle=32,
            labeldistance=1.8,
            fontname="Helvetica"
        ];

	 PERSON [ label=<
        <table border="0" cellborder="1" cellspacing="0">
        <tr><td bgcolor="pink"><b>PERSON</b></td></tr>
        
		<tr><td port="PERSON" align="left" cellpadding="5">PERSON <font color="grey60">int64</font></td></tr>
		<tr><td port="AGE" align="left" cellpadding="5">AGE <font color="grey60">int64</font></td></tr>
		<tr><td port="ADDRESS" align="left" cellpadding="5">ADDRESS <font color="grey60">object</font></td></tr>
		</table>>];

	 CREDIT_CARD [ label=<
        <table border="0" cellborder="1" cellspacing="0">
        <tr><td bgcolor="skyblue"><b>CREDIT_CARD</b></td></tr>
        
		<tr><td port="PERSON" align="left" cellpadding="5">PERSON <font color="grey60">int64</font></td></tr>
		<tr><td port="CREDIT_CARD" align="left" cellpadding="5">CREDIT_CARD <font color="grey60">int64</font></td></tr>
		<tr><td port="DOB" align="left" cellpadding="5">DOB <font color="grey60">object</font></td></tr>
		<tr><td port="PERSON_AGE" align="left" cellpadding="5">PERSON_AGE <font color="grey60">int64</font></td></tr>
		<tr><td port="POSTAL_CODE" align="left" cellpadding="5">POSTAL_CODE <font color="grey60">object</font></td></tr>
		</table>>];

	 PERSON:PERSON->CREDIT_CARD:PERSON [ 
                        arrowhead=ocrow, arrowtail=none];

	 PERSON:AGE->CREDIT_CARD:PERSON_AGE [ 
                        arrowhead=noneotee, arrowtail=noneotee];
	}                  
''')