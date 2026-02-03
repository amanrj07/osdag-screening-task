#3D Bending Moment and Shear Force diagrams
import xarray as xr
import plotly.graph_objects as go
import numpy as np

ds = xr.open_dataset('Xarray_data.nc')
import node_coordinates as nodes_module
import element_connectivity as elements_module

nodes_dict = nodes_module.nodes
elements_dict = elements_module.members

girders = {
    1: [13, 22, 31, 40, 49, 58, 67, 76, 81],
    2: [14, 23, 32, 41, 50, 59, 68, 77, 82],
    3: [15, 24, 33, 42, 51, 60, 69, 78, 83],
    4: [16, 25, 34, 43, 52, 61, 70, 79, 84],
    5: [17, 26, 35, 44, 53, 62, 71, 80, 85]
}

girder_nodes = {
    1: [1, 11, 16, 21, 26, 31, 36, 41, 46, 6],
    2: [2, 12, 17, 22, 27, 32, 37, 42, 47, 7],
    3: [3, 13, 18, 23, 28, 33, 38, 43, 48, 8],
    4: [4, 14, 19, 24, 29, 34, 39, 44, 49, 9],
    5: [5, 15, 20, 25, 30, 35, 40, 45, 50, 10]
}

def create_3d_diagram(diagram_type='Mz'):
    fig = go.Figure()
    
    # Collect data for each girder
    girder_data = {}
    all_values = []
    
    for girder_num in range(1, 6):
        elements = girders[girder_num]
        nodes = girder_nodes[girder_num]
        
        x_coords = []
        z_coords = []
        values = []
        
        for node_id in nodes:
            if node_id in nodes_dict:
                coords = nodes_dict[node_id]
                x_coords.append(coords[0])
                z_coords.append(coords[2])
        
        for i, elem_id in enumerate(elements):
            data = ds['forces'].sel(Element=elem_id)
            
            if diagram_type == 'Mz':
                val_i = float(data.sel(Component='Mz_i').values)
                val_j = float(data.sel(Component='Mz_j').values)
            else:
                val_i = float(data.sel(Component='Vy_i').values)
                val_j = float(data.sel(Component='Vy_j').values)
            
            if i == 0:
                values.append(val_i)
            values.append(val_j)
        
        girder_data[girder_num] = {
            'x': x_coords,
            'z': z_coords,
            'values': values
        }
        all_values.extend(values)
    
    # Get value range for color scaling
    vmin, vmax = min(all_values), max(all_values)
    
    #bridge deck mesh at top (y=0)
    x_all = []
    z_all = []
    for g in girder_data.values():
        x_all.extend(g['x'])
        z_all.extend(g['z'])
    
    x_unique = sorted(list(set(x_all)))
    z_unique = sorted(list(set(z_all)))
    
    X_mesh, Z_mesh = np.meshgrid(x_unique, z_unique)
    Y_mesh = np.zeros_like(X_mesh)
    
    #mesh with wireframe
    fig.add_trace(go.Surface(
        x=X_mesh,
        y=Y_mesh,
        z=Z_mesh,
        surfacecolor=np.zeros_like(X_mesh),
        colorscale=[[0, 'lightgray'], [1, 'lightgray']],
        showscale=False,
        opacity=0.3,
        name='Bridge Deck',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    #mesh grid lines
    for i in range(len(z_unique)):
        fig.add_trace(go.Scatter3d(
            x=X_mesh[i, :],
            y=Y_mesh[i, :],
            z=Z_mesh[i, :],
            mode='lines',
            line=dict(color='gray', width=1),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    for j in range(len(x_unique)):
        fig.add_trace(go.Scatter3d(
            x=X_mesh[:, j],
            y=Y_mesh[:, j],
            z=Z_mesh[:, j],
            mode='lines',
            line=dict(color='gray', width=1),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # 2. Draw vertical colored ribbons/bars below deck for each girder
    scale = 0.05
    
    for girder_num, data in girder_data.items():
        x_coords = data['x']
        z_coords = data['z']
        values = data['values'][:len(x_coords)]
        
        # Normalize values for color
        normalized = [(v - vmin) / (vmax - vmin) if vmax != vmin else 0.5 for v in values]
        
        # Color map: green -> yellow -> red
        def value_to_color(norm_val):
            if norm_val < 0.5:
                # Green to Yellow
                r = int(norm_val * 2 * 255)
                g = 255
                b = 0
            else:
                # Yellow to Red
                r = 255
                g = int((1 - (norm_val - 0.5) * 2) * 255)
                b = 0
            return f'rgb({r},{g},{b})'
        
        # Draw vertical ribbon for this girder
        for i in range(len(x_coords) - 1):
            # Create quad surface between points
            x_quad = [x_coords[i], x_coords[i+1], x_coords[i+1], x_coords[i]]
            z_quad = [z_coords[i], z_coords[i+1], z_coords[i+1], z_coords[i]]
            y_quad = [0, 0, values[i+1] * scale, values[i] * scale]
            
            color = value_to_color(normalized[i])
            
            # Draw filled ribbon
            fig.add_trace(go.Mesh3d(
                x=x_quad,
                y=y_quad,
                z=z_quad,
                i=[0, 0],
                j=[1, 2],
                k=[2, 3],
                color=color,
                opacity=0.8,
                showlegend=False,
                hovertemplate=f'Girder {girder_num}<br>{diagram_type}: {values[i]:.2f}<extra></extra>'
            ))
        
        # Draw outline of force diagram
        y_outline = [v * scale for v in values]
        
        fig.add_trace(go.Scatter3d(
            x=x_coords,
            y=y_outline,
            z=z_coords,
            mode='lines',
            line=dict(color='black', width=3),
            name=f'Girder {girder_num}',
            showlegend=True
        ))
        
        # Draw girder line on deck
        fig.add_trace(go.Scatter3d(
            x=x_coords,
            y=[0] * len(x_coords),
            z=z_coords,
            mode='lines',
            line=dict(color='darkblue', width=4),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Layout
    title = "3D Bending Moment Diagram (BMD)" if diagram_type == 'Mz' else "3D Shear Force Diagram (SFD)"
    unit = "kN·m" if diagram_type == 'Mz' else "kN"
    
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center', font=dict(size=20)),
        scene=dict(
            xaxis=dict(title="X (m)", backgroundcolor="white", gridcolor="lightgray"),
            yaxis=dict(title=f"{diagram_type} ({unit})", backgroundcolor="white", gridcolor="lightgray"),
            zaxis=dict(title="Z (m)", backgroundcolor="white", gridcolor="lightgray"),
            aspectmode='data',
            camera=dict(eye=dict(x=2, y=1.5, z=1.5))
        ),
        height=900,
        showlegend=True,
        legend=dict(x=0.02, y=0.98)
    )
    
    return fig

print("Creating 3D BMD...")
fig_bmd = create_3d_diagram('Mz')
fig_bmd.write_html('task2_3d_bmd.html')
print("✓ Saved task2_3d_bmd.html")

print("\nCreating 3D SFD...")
fig_sfd = create_3d_diagram('Vy')
fig_sfd.write_html('task2_3d_sfd.html')
print("✓ Saved task2_3d_sfd.html")

fig_bmd.show()

print("\n✓ Task 2 Complete!")
print("\nVisualization includes:")
print("  • Bridge deck mesh grid at top")
print("  • Colored vertical ribbons (Green→Yellow→Red)")
print("  • 5 girder force diagrams")
print("  • Interactive 3D rotation")