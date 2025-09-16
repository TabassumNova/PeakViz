import ast
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def viz(batch_name, df_plot, fingerprint_library=None, reference_Spectrums=None,
        sensor='', download=False):
    fig = go.Figure()
    buttons = []
    start = 0
    end = start
    visible_dict = {}
    y_axis_dict = {}
    for key_index, (key, plots) in enumerate(df_plot.items()):
        df = plots[0]
        y_axis_dict[key] = plots[1]
        wavelengths = list(df.columns)[1:]
        data = []
        max_energy = df.iloc[:, 1:].max().max() # For plotting vertical lines
        min_energy = df.iloc[:, 1:].min().min() # For plotting vertical lines
        for index, row in df.iterrows():
            sample_name = list(row)[0]
            energy = list(row)[1:]
            graph = go.Scatter(x=wavelengths, y=energy, name = sample_name, mode='lines',
                               visible=(key_index == 0),
                            #    hoverinfo='x'
                               )
            data.append(graph)
            fig.add_trace(graph)
            end += 1
        
        # Visualisation for Reference Spectrum libraries
        if reference_Spectrums:
            ref_df = reference_Spectrums[key]
            wavelengths = list(ref_df.columns)[1:]
            for index, row in ref_df.iterrows():
                polymer_name = list(row)[0]
                energy = list(row)[1:]
                graph = go.Scatter(x=wavelengths, y=energy, name = polymer_name, mode='lines',
                                visible=(key_index == 0),
                                #    hoverinfo='x'
                                )
                data.append(graph)
                fig.add_trace(graph)
                end += 1
            # TODO: remove redundancy
            max_energy = max(max_energy, ref_df.iloc[:, 1:].max().max()) # For plotting vertical lines 
            min_energy = min(min_energy, ref_df.iloc[:, 1:].min().min()) # For plotting vertical lines  
        
        # Visualisation for fingerprint libraries
        if fingerprint_library is not None:
            lib = fingerprint_library if sensor=='imaging' else fingerprint_library[fingerprint_library['sensor'] == sensor]
            unique_groups = lib['polymer'].unique()
            color_map = {group: px.colors.qualitative.Light24[i % len(px.colors.qualitative.Light24)] for i, group in enumerate(unique_groups)}
            for index, row in lib.iterrows():
                group_name = row['polymer']
                colour = row['colour']
                # Check if the row['wavelengths'] is a string of ranges
                # If yes, then plot shaded area
                if '-' in row['wavelengths']:
                    ranges = row['wavelengths'].strip('[]').split(',')
                    for i, r in enumerate(ranges):
                        r = r.strip()
                        if '-' in r:
                            start_range, end_range = map(float, r.split('-'))
                            shade = go.Scatter(
                                x=[start_range, start_range, end_range, end_range, start_range],
                                y=[min_energy, max_energy, max_energy, min_energy, min_energy],
                                fill='toself',
                                fillcolor='LightSkyBlue',
                                opacity=0.3,
                                mode='lines',
                                line={'color': 'LightSkyBlue'},
                                name=group_name,
                                legendgroup=group_name,
                                showlegend=True if i == 0 else False,
                                visible=(key_index == 0),
                            )
                        data.append(shade)
                        fig.add_trace(shade)
                        end += 1

                else:
                    wavelengths = [float(x) for x in ast.literal_eval(row['wavelengths'])]
                    for i, x_value in enumerate(wavelengths):
                        line = go.Scatter(
                            x=[x_value]*2,  # Duplicate x values for vertical lines
                            y=np.linspace(min_energy, max_energy, num=2).tolist(),  # Alternate y values for vertical lines
                            mode='lines+text',
                            name=group_name,
                            line={'color': colour},
                            legendgroup=group_name,
                            # showlegend=False,
                            showlegend=True if i == 0 else False,
                            visible=(key_index == 0),
                            textposition="top left",
                        )
                        data.append(line)
                        fig.add_trace(line)
                        # Add a vertical line at x=2 using data coordinates
                        
                        end += 1

        visible_dict[key] = (start, end)
        start = end

        

        
    # Buttons for dropdown menu
    for dd_key, limit in visible_dict.items():
        visible = [False] * len(fig.data)
        visible[limit[0] : limit[1]] = [True] * (limit[1]-limit[0])
        buttons.append(dict(
            label=dd_key,
            method="update",
            args=[{"visible": visible},
                  {'yaxis': {'title': y_axis_dict[dd_key]}},
                    {"title": f"{batch_name} : {sensor} - {dd_key}"}]
        ))
    
    # fig.add_annotation(textangle=-90)
    # Add dropdown menu
    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=False,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        )]
    )

    text = batch_name + "_" + sensor
    fig.update_layout(
        # yaxis_range=[0, 1],
        xaxis_title='Wavelength',
        # yaxis_title='Reflectance',
        title={
            'text': batch_name + " : " + sensor,
            'font': {
                'size': 24,
                'color': 'black',
                'family': 'Arial',
                'weight': 'bold'
            },
            'x': 0.5,
            'xanchor': 'center'
        },
    )
    fig.update_layout(hovermode="x unified")
    fig.update_traces(textposition='top center')

    if download:
        fig.write_html(text + ".html")
     
    fig.show()

    