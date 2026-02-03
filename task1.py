#2D Bending Moment and Shear Force diagrams
import xarray as xr
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import node_coordinates as nodes_module
import element_connectivity as elements_module

# Configuration
OUTPUT_FILE = 'task1_output.html'
CENTRAL_GIRDER_ELEMENTS = [15, 24, 33, 42, 51, 60, 69, 78, 83]

def main():
    print("Loading dataset...")
    ds = xr.open_dataset('Xarray_data.nc')
    
    nodes_dict = nodes_module.nodes
    members_dict = elements_module.members
    
    # Data storage
    plot_data_mz = {'x': [], 'y': []}
    plot_data_vy = {'x': [], 'y': []}
    
    print(f"Extracting data for elements: {CENTRAL_GIRDER_ELEMENTS}...")
    
    for i, elem_id in enumerate(CENTRAL_GIRDER_ELEMENTS):
        # Get start and end nodes
        start_node = members_dict[elem_id][0]
        end_node = members_dict[elem_id][1]
        
        # Get X coordinates (Longitudinal position)
        x_start = nodes_dict[start_node][0]
        x_end = nodes_dict[end_node][0]
        
        # Get Mz and Vy forces from dataset
        data = ds['forces'].sel(Element=elem_id)
        mz_i = float(data.sel(Component='Mz_i').values)
        mz_j = float(data.sel(Component='Mz_j').values)
        vy_i = float(data.sel(Component='Vy_i').values)
        vy_j = float(data.sel(Component='Vy_j').values)
        
        # Append data points
        if i == 0:
            plot_data_mz['x'].append(x_start)
            plot_data_mz['y'].append(mz_i)
            plot_data_vy['x'].append(x_start)
            plot_data_vy['y'].append(vy_i)
        
        plot_data_mz['x'].append(x_end)
        plot_data_mz['y'].append(mz_j)
        
        plot_data_vy['x'].append(x_end)
        plot_data_vy['y'].append(vy_j)
    
    print("Creating plots...")
    create_plots(plot_data_mz, plot_data_vy)

def create_plots(data_mz, data_vy):

    fig = make_subplots(
        rows=2, cols=1, 
        subplot_titles=('Bending Moment Diagram (Mz)', 'Shear Force Diagram (Vy)'),
        vertical_spacing=0.15
    )

    # Plot Mz
    fig.add_trace(go.Scatter(
        x=data_mz['x'], 
        y=data_mz['y'], 
        mode='lines+markers', 
        name='Mz', 
        line=dict(color='blue', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(0, 0, 255, 0.1)'
    ), row=1, col=1)

    # Plot Vy
    fig.add_trace(go.Scatter(
        x=data_vy['x'], 
        y=data_vy['y'], 
        mode='lines+markers', 
        name='Vy', 
        line=dict(color='red', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(255, 0, 0, 0.1)'
    ), row=2, col=1)

    # Adding reference lines (y=0)
    fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1, row=1, col=1)
    fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1, row=2, col=1)

    # Updated layout and axes
    fig.update_layout(
        title_text="Central Longitudinal Girder Analysis",
        title_x=0.5,
        height=900, 
        showlegend=False,
        template="plotly_white"
    )

    fig.update_xaxes(title_text="Distance along Bridge (m)", row=1, col=1, showgrid=True)
    fig.update_xaxes(title_text="Distance along Bridge (m)", row=2, col=1, showgrid=True)

    fig.update_yaxes(title_text="Bending Moment (kN·m)", row=1, col=1, showgrid=True)
    fig.update_yaxes(title_text="Shear Force (kN)", row=2, col=1, showgrid=True)

    # Saving output
    fig.write_html(OUTPUT_FILE)
    print(f"Successfully created {OUTPUT_FILE}")

if __name__ == "__main__":
    main() 