import gradio as gr
import httpx
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

conservation_statuses = [
    "Least Concern",
    "Near Threatened",
    "Vulnerable",
    "Endangered",
    "Critically Endangered",
    "Extinct in the Wild",
    "Extinct"
]

families = [
    "Passeridae",
    "Muscicapidae",
    "Tytonidae",
    "Ciconiidae",
    "Accipitridae",
    "Anatidae",
    "Corvidae"
]

def get_species():
    response = httpx.get(f"{BASE_URL}/species/")
    response.raise_for_status()
    return pd.DataFrame(response.json())

def add_species(name, scientific_name, family, conservation_status, wingspan_cm):
    payload = {
        "name": name,
        "scientific_name": scientific_name,
        "family": family,
        "conservation_status": conservation_status,
        "wingspan_cm": wingspan_cm
    }
    response = httpx.post(f"{BASE_URL}/species/", json=payload)
    response.raise_for_status()
    return (
        "Species added successfully",
        get_species()
    )

def get_species_choices():
    response = httpx.get(f"{BASE_URL}/species/")
    response.raise_for_status()
    species_list = response.json()
    return [
        (f"{species['name']} ({species['scientific_name']})", species["id"])
        for species in species_list
    ]

def get_birds():
    response = httpx.get(f"{BASE_URL}/birds/")
    response.raise_for_status()
    return pd.DataFrame(response.json())

def add_bird(nickname, ring_code, age, species_id):
    payload = {
        "nickname": nickname,
        "ring_code": ring_code,
        "age": age,
        "species_id": species_id
    }
    response = httpx.post(f"{BASE_URL}/birds/", json=payload)
    response.raise_for_status()
    return (
        "Bird added successfully",
        get_birds()
    )

def get_bird_choices():
    response = httpx.get(f"{BASE_URL}/birds/")
    response.raise_for_status()
    birds = response.json()
    return [
        (f"{bird['nickname']} ({bird['ring_code']})", bird["id"])
        for bird in birds
    ]

def get_sightings():
    response = httpx.get(f"{BASE_URL}/birdspotting/")
    response.raise_for_status()
    return pd.DataFrame(response.json())

def add_sighting(bird_id, spotted_at, location, observer_name, notes):
    payload = {
        "bird_id": bird_id,
        "spotted_at": spotted_at,
        "location": location,
        "observer_name": observer_name,
        "notes": notes
    }
    response = httpx.post(f"{BASE_URL}/birdspotting/", json=payload)
    response.raise_for_status()
    return "Sighting added successfully", get_sightings()

with gr.Blocks() as demo:
    gr.Markdown("# Bird API integration")
    gr.Markdown("Use this interface to manage species, birds, and sightings.")

    with gr.Tab("Species"):
        gr.Markdown("## Species")
        gr.Markdown("View all species and add a new species.")

        s_name = gr.Textbox(label="Name")
        s_scientific_name = gr.Textbox(label="Scientific name")
        s_family = gr.Dropdown(
            choices=families,
            label="Family",
            allow_custom_value=True,
            filterable=True
        )
        s_status = gr.Dropdown(
            choices=conservation_statuses,
            label="Conservation status"
        )
        s_wingspan = gr.Slider(
            minimum=1,
            maximum=300,
            step=1,
            value=20,
            label="Wingspan (cm)"
        )

        s_add_btn = gr.Button("Add species")
        s_refresh_btn = gr.Button("Refresh species")
        s_message = gr.Textbox(label="Message")
        s_table = gr.DataFrame(label="Species data")

        s_add_btn.click(
            fn=add_species,
            inputs=[s_name, s_scientific_name, s_family, s_status, s_wingspan],
            outputs=[s_message, s_table]
        )

        s_refresh_btn.click(
            fn=get_species,
            inputs=[],
            outputs=s_table
        )

    with gr.Tab("Birds"):
        gr.Markdown("## Birds")
        gr.Markdown("View all birds and add a new bird linked to a species.")

        b_nickname = gr.Textbox(label="Nickname")
        b_ring_code = gr.Textbox(label="Ring code")
        b_age = gr.Number(label="Age", minimum=0, value=1)
        b_species = gr.Dropdown(
            choices=get_species_choices(),
            label="Species"
        )

        b_add_btn = gr.Button("Add bird")
        b_refresh_btn = gr.Button("Refresh birds")
        b_message = gr.Textbox(label="Message")
        b_table = gr.DataFrame(label="Bird data")

        b_add_btn.click(
            fn=add_bird,
            inputs=[b_nickname, b_ring_code, b_age, b_species],
            outputs=[b_message, b_table]
        )

        b_refresh_btn.click(
            fn=lambda: [get_birds(), gr.update(choices=get_species_choices())],
            inputs=[],
            outputs=[b_table, b_species]
        )

    with gr.Tab("Sightings"):
        gr.Markdown("## Sightings")
        gr.Markdown("View all sightings and add a new sighting linked to a bird.")

        bs_bird = gr.Dropdown(
            choices=get_bird_choices(),
            label="Bird"
        )
        bs_spotted_at = gr.Textbox(
            label="Spotted at",
            value="2026-03-30T14:00:00"
        )
        bs_location = gr.Textbox(label="Location")
        bs_observer = gr.Textbox(label="Observer name")
        bs_notes = gr.Textbox(label="Notes")

        bs_add_btn = gr.Button("Add sighting")
        bs_refresh_btn = gr.Button("Refresh sightings")
        bs_message = gr.Textbox(label="Message")
        bs_table = gr.DataFrame(label="Sightings data")

        bs_add_btn.click(
            fn=add_sighting,
            inputs=[bs_bird, bs_spotted_at, bs_location, bs_observer, bs_notes],
            outputs=[bs_message, bs_table]
        )

        bs_refresh_btn.click(
            fn=lambda: [gr.update(choices=get_bird_choices()), get_sightings()],
            inputs=[],
            outputs=[bs_bird, bs_table]
        )

demo.launch()