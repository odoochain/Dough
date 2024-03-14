import time
import streamlit as st
from ui_components.constants import CreativeProcessType
from ui_components.widgets.timeline_view import timeline_view
from ui_components.components.explorer_page import gallery_image_view
from streamlit_option_menu import option_menu
from utils import st_memory
from utils.data_repo.data_repo import DataRepo
from ui_components.widgets.sidebar_logger import sidebar_logger
from ui_components.components.explorer_page import generate_images_element

def timeline_view_page(shot_uuid: str, h2):
    data_repo = DataRepo()
    shot = data_repo.get_shot_from_uuid(shot_uuid)
    project_uuid = shot.project.uuid
    project = data_repo.get_project_from_uuid(project_uuid)

    with st.sidebar:
        views = CreativeProcessType.value_list()

        if "view" not in st.session_state:
            st.session_state["view"] = views[0]

        st.write("")    

        with st.expander("🔍 Generation log", expanded=True):
            # if st_memory.toggle("Open", value=True, key="generaton_log_toggle"):
            sidebar_logger(st.session_state["shot_uuid"])
        
        st.write("")

        with st.expander("📋 Explorer shortlist",expanded=True):
            if st_memory.toggle("Open", value=True, key="explorer_shortlist_toggle"):
                gallery_image_view(shot.project.uuid, shortlist=True, view=["add_and_remove_from_shortlist","add_to_any_shot"])
        
    st.markdown(f"#### :green[{st.session_state['main_view_type']}] > :red[{st.session_state['page']}]")
    st.markdown("***")
    slider1, slider2 = st.columns([4,1])
    with slider1:
        st.markdown(f"### 🪄 '{project.name}' timeline")
        st.write("##### _\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_")

    # start_time = time.time()
    timeline_view(st.session_state["shot_uuid"], st.session_state['view'])
    st.markdown("### ✨ Generate frames")
    st.write("##### _\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_")
    
    # end_time = time.time()
    # print("///////////////// timeline laoded in: ", end_time - start_time)
    generate_images_element(position='explorer', project_uuid=project_uuid, timing_uuid=None, shot_uuid=None)
    # end_time = time.time()
    # print("///////////////// generate img laoded in: ", end_time - start_time)
    gallery_image_view(project_uuid,False,view=['add_and_remove_from_shortlist','view_inference_details','shot_chooser','add_to_any_shot'])
    # end_time = time.time()
    # print("///////////////// gallery laoded in: ", end_time - start_time)