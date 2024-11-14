# app/views.py
from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    plot_size = request.form.get('plotSize')
    bedrooms = int(request.form.get('bedrooms'))
    bathrooms = int(request.form.get('bathrooms'))
    kitchens = int(request.form.get('kitchens'))
    additional_rooms = request.form.get('additionalRooms')
    preferences = request.form.get('preferences')

    # Predefined plot sizes
    plot_sizes = {
        "30x40": (30, 40),
        "40x60": (40, 60)
    }

    # Get plot dimensions based on selected plot size
    dimensions = plot_sizes.get(plot_size)
    if dimensions is None:
        return "Invalid plot size selected.", 400  # Return a 400 Bad Request error if the plot size is not found

    plot_width, plot_height = dimensions

    # Ensure the longer side is horizontal
    if plot_height > plot_width:
        plot_width, plot_height = plot_height, plot_width

    # Calculate house dimensions with 3 feet setback on all sides
    house_width = plot_width - 6
    house_height = plot_height - 6

    # Draw the plot outline using matplotlib
    fig, ax = plt.subplots()
    plot_outline = plt.Rectangle((0, 0), plot_width, plot_height, linewidth=3, edgecolor='black', facecolor='none')
    ax.add_patch(plot_outline)

    # Draw the house boundary inside the plot
    house_outline = plt.Rectangle((3, 3), house_width, house_height, linewidth=3, edgecolor='black', facecolor='none')
    ax.add_patch(house_outline)

    # Add "Living Room" label to the house
    ax.text(3 + house_width / 2, 3 + house_height / 2, "Living Room", ha='center', va='center', fontsize=10, color='black')

    # Add dimension labels on the respective sides
    ax.text(plot_width / 2, -1, f'{plot_width} ft', ha='center', va='top', fontsize=10, color='black')
    ax.text(-1, plot_height / 2, f'{plot_height} ft', ha='right', va='center', fontsize=10, color='black')
    ax.text(plot_width / 2, plot_height + 1, f'{plot_width} ft', ha='center', va='bottom', fontsize=10, color='black')
    ax.text(plot_width + 1, plot_height / 2, f'{plot_height} ft', ha='left', va='center', fontsize=10, color='black')

    # Set the limits of the plot
    ax.set_xlim(0, plot_width)
    ax.set_ylim(0, plot_height)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')  # Turn off the axis

    # Draw the outer boundary of the plot to make it consistent
    ax.plot([0, plot_width, plot_width, 0, 0], [0, 0, plot_height, plot_height, 0], color='black', linewidth=3)

    # Save the plot
    plot_path = os.path.join('app', 'static', 'plot.png')
    fig.savefig(plot_path, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

    return render_template('result.html', plot_image=plot_path)

if __name__ == '__main__':
    app.run(debug=True)