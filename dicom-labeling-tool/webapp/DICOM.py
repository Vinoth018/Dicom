# import streamlit as st
# from src.utils import *
# import gc
# import numpy as np
# from scipy import ndimage
# from skimage.transform import resize
# # Hide FileUploader deprecation
# st.set_option('deprecation.showfileUploaderEncoding', False)

# # Hide streamlit header
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """

# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# data_key = 'has_data'
# width = 400
# data_is_ready = False
# data_has_changed = False

# if not os.path.isdir('./data/'):
#     os.makedirs('./data/')

# if not os.path.isdir('./temp'):
#     os.makedirs('./temp/')

# # Adjusting images to be centralized.
# with open("style.css") as f:
#     st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    
# if __name__ == "__main__": 
    
#     state = get_state()

#     st.title('DICOM Viewer')

#     st.sidebar.title('DICOM Image Viewer')

#     demo_button = st.sidebar.checkbox('Demo', value=False, key='demo_checkbox')
    
#     url_input = st.sidebar.text_input('Enter the Google Drive shared url for the .dcm files', key='url_input')
    
#     st.sidebar.markdown('<h5>MAX FILE SIZE: 100 MB</h5>', unsafe_allow_html=True)
#     st.sidebar.markdown(' ')
#     st.sidebar.markdown('or')

#     file_uploaded =  st.sidebar.file_uploader("Upload a .zip with .dcm files (slower than GDrive)", type="zip", key='file_uploader')

#     if demo_button:
#         url_input = 'https://drive.google.com/file/d/1ESRZpJA92g8L4PqT2adCN3hseFbnw9Hg/view?usp=sharing'

#     if file_uploaded:
#         if not state[data_key]:
#             if does_zip_have_dcm(file_uploaded):
#                 store_data(file_uploaded)
#                 data_has_changed = True
    
#     if url_input:
#         if not state[data_key]:
#             if download_zip_from_url(url_input):
#                 data_has_changed = True

#     if st.sidebar.button('---------- Refresh input data ----------', key='refresh_button'):
#         clear_data_storage(temp_data_directory + get_report_ctx().session_id + '/')
#         clear_data_storage(temp_zip_folder)
#         st.caching.clear_cache()
#         url_input = st.empty()
#         data_is_ready = False
#         data_has_changed = False
#         state[data_key] = False
#         state.clear()

#     if data_has_changed:
#         valid_folders = get_DCM_valid_folders(temp_data_directory + get_report_ctx().session_id + '/')
        
#         for folder in valid_folders:
#             state[folder.split('/')[-1]] = ('', '', {'Anomaly': 'Bleeding', 'Slices': ''})

#         state[data_key] = True
#         state['valid_folders'] = valid_folders
#         state.last_serie = ''

#         data_has_changed = False
    
#     if state[data_key]:
#         data_is_ready = True
    
#     if data_is_ready:
#         series_names = get_series_names(state['valid_folders'])
        
#         selected_serie = st.selectbox('Select a series', series_names, index=0, key='select_series')

#         st.markdown('<h2>Patient Info</h2>', unsafe_allow_html=True)
#         display_info = st.checkbox('Display data', value=True)

#         if state.last_serie != selected_serie:
#             st.caching.clear_cache()
#             state.last_serie = selected_serie

#         img3d, info = processing_data(state['valid_folders'][series_names.index(selected_serie)] + '/')
            
#         if display_info:
#             st.dataframe(info)
        
#         slice_slider = st.slider(
#             'Slices',
#             0, img3d.shape[2] - 1, (img3d.shape[2] - 1)//2,
#             key='slice_slider'
#         )

#         color_threshold = st.slider(
#             'Color Threshold',
#             0, 100, 50,
#             key='color_threshold_slider'
#         )
#         def rotate_and_resize(image, angle, size):
#             rotated = ndimage.rotate(image, angle)
#             resized = resize(rotated, size)
#             return resized

#         axial_max = int(img3d[:, :, slice_slider].max())
#         axial_threshold = axial_max * ((2 * color_threshold / 100) - 1)
#         axial_slice = normalize_image(filter_image(axial_threshold, img3d[:, :, slice_slider]))

#         coronal_max = int(img3d[slice_slider, :, :].max())
#         coronal_threshold = coronal_max * ((2 * color_threshold / 100) - 1)
#         coronal_slice = normalize_image(filter_image(coronal_threshold, rotate_and_resize(img3d[slice_slider, :, :], 90, (img3d.shape[0], img3d.shape[0]))))

#         sagittal_max = int(img3d[:, slice_slider, :].max())
#         sagittal_threshold = sagittal_max * ((2 * color_threshold / 100) - 1)
#         sagittal_slice = normalize_image(filter_image(sagittal_threshold, rotate_and_resize(img3d[:, slice_slider, :], 90, (img3d.shape[0], img3d.shape[0]))))

#         #  Display the slices horizontally
#         st.image([axial_slice, coronal_slice, sagittal_slice], caption=['Axial Slice {}'.format(slice_slider), 'Coronal Slice {}'.format(slice_slider), 'Sagittal Slice {}'.format(slice_slider)], width=width)
        
        
       

#         st.sidebar.markdown('<h1 style=\'font-size:0.65em\'> Example of annotation with slices: 0-11; 57-59; 112; </h1> ', unsafe_allow_html=True)

#         state[selected_serie][2]['Anomaly'] = st.sidebar.text_input('Anomaly Label', value=state[selected_serie][2]['Anomaly'], key='anomaly_label')

#         state[selected_serie][2]['Slices'] = st.sidebar.text_input("Axial Annotation - Slices with Anomaly", value=state[selected_serie][2]['Slices'], key='axial_annotation_input')

#         annotation_selected = st.sidebar.multiselect('Annotated series to be included in the .json', series_names, series_names, key='annotation_multiselect')
#         json_selected = {serie: state[serie][2] for serie in annotation_selected}
        
#         if st.checkbox('Check Annotations.json', value=True):
#             st.write(json_selected)
        
#         download_button_str = download_button(json_selected, 'Annotation.json', 'Download Annotation.json')
#         st.sidebar.markdown(download_button_str, unsafe_allow_html=True) 

#         del img3d, info

#     if st.sidebar.checkbox('Notes', value=True, key='otes_checkbox'):
#         st.sidebar.markdown('1. It does not recognize zip folders inside other zip folders.')
#         st.sidebar.markdown('2. It only recognizes series with two or more .dcm files.')
#         st.sidebar.markdown('3. You can use the arrow keys to change the slider widgets.')
#         st.sidebar.markdown('3. Uploaded files are cached until the heroku session becomes idle (30 min).'
#                             ' Then, they are automatically deleted.')
#         st.sidebar.markdown('4. If you want to manually reset/delete previously uploaded data via URL, ' 
#                             'clear the text input, and press the button to refresh input data. '
#                             'In case you are using the File Uploader widget, perform the same '
#                             'actions described above and then refresh the page with F5. ')
    
#     gc.collect()
#     state.sync()
































# import os
# from flask import Flask, render_template, request, send_file
# from src.utils import *
# import gc
# import numpy as np
# from scipy import ndimage
# from skimage.transform import resize

# app = Flask(__name__)

# # Hide FileUploader deprecation
# app.config['UPLOAD_FOLDER'] = './uploads'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/process_data', methods=['POST'])
# def process_data():
#     data_key = 'has_data'
#     width = 400
#     data_is_ready = False
#     data_has_changed = False
#     temp_data_directory = './temp/'
#     temp_zip_folder = './temp_zip/'
#     state = get_state()

#     if not os.path.isdir('./data/'):
#         os.makedirs('./data/')

#     if not os.path.isdir(temp_data_directory):
#         os.makedirs(temp_data_directory)

#     if not os.path.isdir(temp_zip_folder):
#         os.makedirs(temp_zip_folder)

#     if request.method == 'POST':
#         file = request.files['file']
#         url_input = request.form['url_input']
#         demo_button = request.form.get('demo_button') == 'on'

#         if demo_button:
#             url_input = 'https://drive.google.com/file/d/1ESRZpJA92g8L4PqT2adCN3hseFbnw9Hg/view?usp=sharing'

#         if file:
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(file_path)
#             if not state[data_key]:
#                 if does_zip_have_dcm(file_path):
#                     store_data(file_path)
#                     data_has_changed = True
#         elif url_input:
#             if not state[data_key]:
#                 if download_zip_from_url(url_input):
#                     data_has_changed = True

#     if data_has_changed:
#         valid_folders = get_DCM_valid_folders(temp_data_directory + get_report_ctx().session_id + '/')
        
#         for folder in valid_folders:
#             state[folder.split('/')[-1]] = ('', '', {'Anomaly': 'Bleeding', 'Slices': ''})

#         state[data_key] = True
#         state['valid_folders'] = valid_folders
#         state.last_serie = ''

#         data_has_changed = False
    
#     if state[data_key]:
#         data_is_ready = True
    
#     if data_is_ready:
#         series_names = get_series_names(state['valid_folders'])
        
#         selected_serie = request.form['selected_serie']

#         img3d, info = processing_data(state['valid_folders'][series_names.index(selected_serie)] + '/')
            
#         slice_slider = request.form.get('slice_slider', (img3d.shape[2] - 1)//2)
#         color_threshold = request.form.get('color_threshold_slider', 50)

#         def rotate_and_resize(image, angle, size):
#             rotated = ndimage.rotate(image, angle)
#             resized = resize(rotated, size)
#             return resized

#         axial_max = int(img3d[:, :, slice_slider].max())
#         axial_threshold = axial_max * ((2 * int(color_threshold) / 100) - 1)
#         axial_slice = normalize_image(filter_image(axial_threshold, img3d[:, :, slice_slider]))

#         coronal_max = int(img3d[slice_slider, :, :].max())
#         coronal_threshold = coronal_max * ((2 * int(color_threshold) / 100) - 1)
#         coronal_slice = normalize_image(filter_image(coronal_threshold, rotate_and_resize(img3d[slice_slider, :, :], 90, (img3d.shape[0], img3d.shape[0]))))

#         sagittal_max = int(img3d[:, slice_slider, :].max())
#         sagittal_threshold = sagittal_max * ((2 * int(color_threshold) / 100) - 1)
#         sagittal_slice = normalize_image(filter_image(sagittal_threshold, rotate_and_resize(img3d[:, slice_slider, :], 90, (img3d.shape[0], img3d.shape[0]))))

#         gc.collect()
#         state.sync()

#         return render_template('result.html', 
#                                 selected_serie=selected_serie, 
#                                 axial_slice=axial_slice, 
#                                 coronal_slice=coronal_slice, 
#                                 sagittal_slice=sagittal_slice)
#     else:
#         return render_template('result.html')

# @app.route('/download_annotation')
# def download_annotation():
#     # Logic to generate and download the annotation.json file
#     return send_file(annotation_path, as_attachment=True)

# if __name__ == "__main__":
#     app.run(debug=True)

##################################################################################################
# import streamlit as st
# from src.utils import *
# import gc
# import numpy as np
# from scipy import ndimage
# from skimage.transform import resize
# import json
# import os
# import base64

# # Hide FileUploader deprecation
# st.set_option('deprecation.showfileUploaderEncoding', False)

# # Hide streamlit header
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """

# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# data_key = 'has_data'
# width = 400
# data_is_ready = False
# data_has_changed = False

# if not os.path.isdir('./data/'):
#     os.makedirs('./data/')

# if not os.path.isdir('./temp'):
#     os.makedirs('./temp/')

# # Adjusting images to be centralized.
# with open("style.css") as f:
#     st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    
# def get_binary_file_downloader_html(bin_file, file_label='File'):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     bin_str = base64.b64encode(data).decode()
#     href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
#     return href
    
# if __name__ == "__main__":

    
#     state = get_state()

#     st.title('DICOM Viewer')

#     st.sidebar.title('DICOM Image Viewer')

#     demo_button = st.sidebar.checkbox('Demo', value=False, key='demo_checkbox')
    
#     url_input = st.sidebar.text_input('Enter the Google Drive shared url for the .dcm files', key='url_input')
    
#     st.sidebar.markdown('<h5>MAX FILE SIZE: 100 MB</h5>', unsafe_allow_html=True)
#     st.sidebar.markdown(' ')
#     st.sidebar.markdown('or')

#     file_uploaded =  st.sidebar.file_uploader("Upload a .zip with .dcm files (slower than GDrive)", type="zip", key='file_uploader')

#     if demo_button:
#         url_input = 'https://drive.google.com/file/d/1ESRZpJA92g8L4PqT2adCN3hseFbnw9Hg/view?usp=sharing'

#     if file_uploaded:
#         if not state[data_key]:
#             if does_zip_have_dcm(file_uploaded):
#                 store_data(file_uploaded)
#                 data_has_changed = True
    
#     if url_input:
#         if not state[data_key]:
#             if download_zip_from_url(url_input):
#                 data_has_changed = True

#     if st.sidebar.button('---------- Refresh input data ----------', key='refresh_button'):
#         clear_data_storage(temp_data_directory + get_report_ctx().session_id + '/')
#         clear_data_storage(temp_zip_folder)
#         st.caching.clear_cache()
#         url_input = st.empty()
#         data_is_ready = False
#         data_has_changed = False
#         state[data_key] = False
#         state.clear()

#     if data_has_changed:
#         valid_folders = get_DCM_valid_folders(temp_data_directory + get_report_ctx().session_id + '/')
        
#         for folder in valid_folders:
#             state[folder.split('/')[-1]] = ('', '', {'Anomaly': 'Bleeding', 'Slices': ''})

#         state[data_key] = True
#         state['valid_folders'] = valid_folders
#         state.last_serie = ''

#         data_has_changed = False
    
#     if state[data_key]:
#         data_is_ready = True
    
#     if data_is_ready:
#         series_names = get_series_names(state['valid_folders'])
        
#         selected_serie = st.selectbox('Select a series', series_names, index=0, key='select_series')

#         st.markdown('<h2>Patient Info</h2>', unsafe_allow_html=True)
#         display_info = st.checkbox('Display data', value=True)

#         if state.last_serie != selected_serie:
#             st.caching.clear_cache()
#             state.last_serie = selected_serie

#         img3d, info = processing_data(state['valid_folders'][series_names.index(selected_serie)] + '/')
            
#         if display_info:
#             st.dataframe(info)

        
#         slice_slider = st.slider(
#             'Slices',
#             0, img3d.shape[2] - 1, (img3d.shape[2] - 1)//2,
#             key='slice_slider'
#         )

#         color_threshold = st.slider(
#             'Color Threshold',
#             0, 100, 50,
#             key='color_threshold_slider'
#         )
#         def rotate_and_resize(image, angle, size):
#             rotated = ndimage.rotate(image, angle)
#             resized = resize(rotated, size)
#             return resized

#         axial_max = int(img3d[:, :, slice_slider].max())
#         axial_threshold = axial_max * ((2 * color_threshold / 100) - 1)
#         axial_slice = normalize_image(filter_image(axial_threshold, img3d[:, :, slice_slider]))

#         coronal_max = int(img3d[slice_slider, :, :].max())
#         coronal_threshold = coronal_max * ((2 * color_threshold / 100) - 1)
#         coronal_slice = normalize_image(filter_image(coronal_threshold, rotate_and_resize(img3d[slice_slider, :, :]
# , 90, (img3d.shape[0], img3d.shape[0]))))

#         sagittal_max = int(img3d[:, slice_slider, :].max())
#         sagittal_threshold = sagittal_max * ((2 * color_threshold / 100) - 1)
#         sagittal_slice = normalize_image(filter_image(sagittal_threshold, rotate_and_resize(img3d[:, slice_slider, :]
# , 90, (img3d.shape[0], img3d.shape[0]))))

#         #  Display the slices horizontally
#         st.image([axial_slice, coronal_slice, sagittal_slice], caption=['Axial Slice {}'.format(slice_slider), 'Coronal Slice {}'.format(slice_slider), 'Sagittal Slice {}'.format(slice_slider)], width=width)
        
#         st.sidebar.markdown('<h1 style=\'font-size:0.65em\'> Example of annotation with slices: 0-11; 57-59; 112; </h1> ', unsafe_allow_html=True)

#         state[selected_serie][2]['Anomaly'] = st.sidebar.text_input('Anomaly Label', value=state[selected_serie][2]['Anomaly'], key='anomaly_label')

#         state[selected_serie][2]['Slices'] = st.sidebar.text_input("Axial Annotation - Slices with Anomaly", value=state[selected_serie][2]['Slices'], key='axial_annotation_input')

#         annotation_selected = st.sidebar.multiselect('Annotated series to be included in the .json', series_names, series_names, key='annotation_multiselect')
#         json_selected = {serie: state[serie][2] for serie in annotation_selected}
        
#         if st.checkbox('Check Annotations.json', value=True):
#             st.write(json_selected)
        
#         download_button_str = download_button(json_selected, 'Annotation.json', 'Download Annotation.json')
#         st.sidebar.markdown(download_button_str, unsafe_allow_html=True) 

#         # Export button for JSON data
#         if st.sidebar.button('Export Annotations as JSON'):
#             with open('Annotation.json', 'w') as json_file:
#                 json.dump(json_selected, json_file)
#             st.sidebar.markdown(get_binary_file_downloader_html('Annotation.json', 'JSON'), unsafe_allow_html=True)

#         # Export button for Images
#         if st.sidebar.button('Export Images'):
#             # Save the axial slice as an image file
#             axial_slice_filename = 'Axial_Slice_{}.png'.format(slice_slider)
#             axial_slice_path = os.path.join('./', axial_slice_filename)
#             st.image(axial_slice, caption='Axial Slice', use_column_width=True)
#             st.write('Downloading Axial Slice as:', axial_slice_filename)
#             with open(axial_slice_path, 'wb') as f:
#                 f.write(axial_slice)

#             # Save the coronal slice as an image file
#             coronal_slice_filename = 'Coronal_Slice_{}.png'.format(slice_slider)
#             coronal_slice_path = os.path.join('./', coronal_slice_filename)
#             st.image(coronal_slice, caption='Coronal Slice', use_column_width=True)
#             st.write('Downloading Coronal Slice as:', coronal_slice_filename)
#             with open(coronal_slice_path, 'wb') as f:
#                 f.write(coronal_slice)

#             # Save the sagittal slice as an image file
#             sagittal_slice_filename = 'Sagittal_Slice_{}.png'.format(slice_slider)
#             sagittal_slice_path = os.path.join('./', sagittal_slice_filename)
#             st.image(sagittal_slice, caption='Sagittal Slice', use_column_width=True)
#             st.write('Downloading Sagittal Slice as:', sagittal_slice_filename)
#             with open(sagittal_slice_path, 'wb') as f:
#                 f.write(sagittal_slice)

#             st.markdown(get_binary_file_downloader_html(axial_slice_path, 'Axial Slice'), unsafe_allow_html=True)
#             st.markdown(get_binary_file_downloader_html(coronal_slice_path, 'Coronal Slice'), unsafe_allow_html=True)
#             st.markdown(get_binary_file_downloader_html(sagittal_slice_path, 'Sagittal Slice'), unsafe_allow_html=True)
     
#         del img3d, info

#     if st.sidebar.checkbox('Notes'):
#         st.sidebar.markdown('1. It does not recognize zip folders inside other zip folders.')
#         st.sidebar.markdown('2. It only recognizes series with two or more .dcm files.')
#         st.sidebar.markdown('3. You can use the arrow keys to change the slider widgets.')
#         st.sidebar.markdown('3. Uploaded files are cached until the heroku session becomes idle (30 min).'
#                             ' Then, they are automatically deleted.')
#         st.sidebar.markdown('4. If you want to manually reset/delete previously uploaded data via URL, ' 
#                             'clear the text input, and press the button to refresh input data. '
#                             'In case you are using the File Uploader widget, perform the same '
#                             'actions described above and then refresh the page with F5. ')
    
#     gc.collect()
#     state.sync()
#################################################
# import streamlit as st
# from src.utils import *
# import gc
# import numpy as np
# from scipy import ndimage
# from skimage.transform import resize
# import json
# import os
# import base64

# # Hide FileUploader deprecation
# st.set_option('deprecation.showfileUploaderEncoding', False)

# # Hide streamlit header
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """

# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# data_key = 'has_data'
# width = 400
# data_is_ready = False
# data_has_changed = False

# if not os.path.isdir('./data/'):
#     os.makedirs('./data/')

# if not os.path.isdir('./temp'):
#     os.makedirs('./temp/')

# # Adjusting images to be centralized.
# with open("style.css") as f:
#     st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    
# def get_binary_file_downloader_html(bin_file, file_label='File'):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     bin_str = base64.b64encode(data).decode()
#     href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
#     return href
    
# if __name__ == "__main__":

    
#     state = get_state()

#     st.title('DICOM Viewer')

#     st.sidebar.title('DICOM Image Viewer')

#     demo_button = st.sidebar.checkbox('Demo', value=False, key='demo_checkbox')
    
#     url_input = st.sidebar.text_input('Enter the Google Drive shared url for the .dcm files', key='url_input')
    
#     st.sidebar.markdown('<h5>MAX FILE SIZE: 100 MB</h5>', unsafe_allow_html=True)
#     st.sidebar.markdown(' ')
#     st.sidebar.markdown('or')

#     file_uploaded =  st.sidebar.file_uploader("Upload a .zip with .dcm files (slower than GDrive)", type="zip", key='file_uploader')

#     if demo_button:
#         url_input = 'https://drive.google.com/file/d/1ESRZpJA92g8L4PqT2adCN3hseFbnw9Hg/view?usp=sharing'

#     if file_uploaded:
#         if not state[data_key]:
#             if does_zip_have_dcm(file_uploaded):
#                 store_data(file_uploaded)
#                 data_has_changed = True
    
#     if url_input:
#         if not state[data_key]:
#             if download_zip_from_url(url_input):
#                 data_has_changed = True

#     if st.sidebar.button('---------- Refresh input data ----------', key='refresh_button'):
#         clear_data_storage(temp_data_directory + get_report_ctx().session_id + '/')
#         clear_data_storage(temp_zip_folder)
#         st.caching.clear_cache()
#         url_input = st.empty()
#         data_is_ready = False
#         data_has_changed = False
#         state[data_key] = False
#         state.clear()

#     if data_has_changed:
#         valid_folders = get_DCM_valid_folders(temp_data_directory + get_report_ctx().session_id + '/')
        
#         for folder in valid_folders:
#             state[folder.split('/')[-1]] = ('', '', {'Anomaly': 'Bleeding', 'Slices': ''})

#         state[data_key] = True
#         state['valid_folders'] = valid_folders
#         state.last_serie = ''

#         data_has_changed = False
    
#     if state[data_key]:
#         data_is_ready = True
    
#     if data_is_ready:
#         series_names = get_series_names(state['valid_folders'])
        
#         selected_serie = st.selectbox('Select a series', series_names, index=0, key='select_series')

#         st.markdown('<h2>Patient Info</h2>', unsafe_allow_html=True)
#         display_info = st.checkbox('Display data', value=True)

#         if state.last_serie != selected_serie:
#             st.caching.clear_cache()
#             state.last_serie = selected_serie

#         img3d, info = processing_data(state['valid_folders'][series_names.index(selected_serie)] + '/')
            
#         if display_info:
#             st.dataframe(info)

        
#         slice_slider = st.slider(
#             'Slices',
#             0, img3d.shape[2] - 1, (img3d.shape[2] - 1)//2,
#             key='slice_slider'
#         )

#         color_threshold = st.slider(
#             'Color Threshold',
#             0, 100, 50,
#             key='color_threshold_slider'
#         )
#         def rotate_and_resize(image, angle, size):
#             rotated = ndimage.rotate(image, angle)
#             resized = resize(rotated, size)
#             return resized

#         axial_max = int(img3d[:, :, slice_slider].max())
#         axial_threshold = axial_max * ((2 * color_threshold / 100) - 1)
#         axial_slice = normalize_image(filter_image(axial_threshold, img3d[:, :, slice_slider]))

#         coronal_max = int(img3d[slice_slider, :, :].max())
#         coronal_threshold = coronal_max * ((2 * color_threshold / 100) - 1)
#         coronal_slice = normalize_image(filter_image(coronal_threshold, rotate_and_resize(img3d[slice_slider, :, :]
# , 90, (img3d.shape[0], img3d.shape[0]))))

#         sagittal_max = int(img3d[:, slice_slider, :].max())
#         sagittal_threshold = sagittal_max * ((2 * color_threshold / 100) - 1)
#         sagittal_slice = normalize_image(filter_image(sagittal_threshold, rotate_and_resize(img3d[:, slice_slider, :]
# , 90, (img3d.shape[0], img3d.shape[0]))))

#         #  Display the slices horizontally
#         st.image([axial_slice, coronal_slice, sagittal_slice], caption=['Axial Slice {}'.format(slice_slider), 'Coronal Slice {}'.format(slice_slider), 'Sagittal Slice {}'.format(slice_slider)], width=width)
        
#         st.sidebar.markdown('<h1 style=\'font-size:0.65em\'> Example of annotation with slices: 0-11; 57-59; 112; </h1> ', unsafe_allow_html=True)

#         state[selected_serie][2]['Anomaly'] = st.sidebar.text_input('Anomaly Label', value=state[selected_serie][2]['Anomaly'], key='anomaly_label')

#         state[selected_serie][2]['Slices'] = st.sidebar.text_input("Axial Annotation - Slices with Anomaly", value=state[selected_serie][2]['Slices'], key='axial_annotation_input')

#         annotation_selected = st.sidebar.multiselect('Annotated series to be included in the .json', series_names, series_names, key='annotation_multiselect')
#         json_selected = {serie: state[serie][2] for serie in annotation_selected}
        
#         if st.checkbox('Check Annotations.json', value=True):
#             st.write(json_selected)
        
#         download_button_str = download_button(json_selected, 'Annotation.json', 'Download Annotation.json')
#         st.sidebar.markdown(download_button_str, unsafe_allow_html=True) 

#         # Export button for JSON data
#         if st.sidebar.button('Export Annotations as JSON'):
#             with open('Annotation.json', 'w') as json_file:
#                 json.dump(json_selected, json_file)
#             st.sidebar.markdown(get_binary_file_downloader_html('Annotation.json', 'JSON'), unsafe_allow_html=True)

#         # Export button for Images
#         if st.sidebar.button('Export Images'):
#             # Save the axial slice as an image file
#             axial_slice_filename = 'Axial_Slice_{}.dcm'.format(slice_slider)
#             axial_slice_path = os.path.join('./', axial_slice_filename)
#             st.image(axial_slice, caption='Axial Slice', use_column_width=True)
#             st.write('Downloading Axial Slice as:', axial_slice_filename)
#             with open(axial_slice_path, 'wb') as f:
#                 f.write(axial_slice)

#             # Save the coronal slice as an image file
#             coronal_slice_filename = 'Coronal_Slice_{}.png'.format(slice_slider)
#             coronal_slice_path = os.path.join('./', coronal_slice_filename)
#             st.image(coronal_slice, caption='Coronal Slice', use_column_width=True)
#             st.write('Downloading Coronal Slice as:', coronal_slice_filename)
#             with open(coronal_slice_path, 'wb') as f:
#                 f.write(coronal_slice)

#             # Save the sagittal slice as an image file
#             sagittal_slice_filename = 'Sagittal_Slice_{}.png'.format(slice_slider)
#             sagittal_slice_path = os.path.join('./', sagittal_slice_filename)
#             st.image(sagittal_slice, caption='Sagittal Slice', use_column_width=True)
#             st.write('Downloading Sagittal Slice as:', sagittal_slice_filename)
#             with open(sagittal_slice_path, 'wb') as f:
#                 f.write(sagittal_slice)

#             st.markdown(get_binary_file_downloader_html(axial_slice_path, 'Axial Slice'), unsafe_allow_html=True)
#             st.markdown(get_binary_file_downloader_html(coronal_slice_path, 'Coronal Slice'), unsafe_allow_html=True)
#             st.markdown(get_binary_file_downloader_html(sagittal_slice_path, 'Sagittal Slice'), unsafe_allow_html=True)
     
#         del img3d, info

#     if st.sidebar.checkbox('Notes'):
#         st.sidebar.markdown('1. It does not recognize zip folders inside other zip folders.')
#         st.sidebar.markdown('2. It only recognizes series with two or more .dcm files.')
#         st.sidebar.markdown('3. You can use the arrow keys to change the slider widgets.')
#         st.sidebar.markdown('3. Uploaded files are cached until the heroku session becomes idle (30 min).'
#                             ' Then, they are automatically deleted.')
#         st.sidebar.markdown('4. If you want to manually reset/delete previously uploaded data via URL, ' 
#                             'clear the text input, and press the button to refresh input data. '
#                             'In case you are using the File Uploader widget, perform the same '
#                             'actions described above and then refresh the page with F5. ')
    
#     gc.collect()
#     state.sync()
#################################one zip but not working
# import streamlit as st
# from src.utils import *
# import gc
# import numpy as np
# from scipy import ndimage
# from skimage.transform import resize
# import json
# import os
# import base64
# import zipfile

# # Hide FileUploader deprecation
# st.set_option('deprecation.showfileUploaderEncoding', False)

# # Hide streamlit header
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """

# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# data_key = 'has_data'
# width = 400
# data_is_ready = False
# data_has_changed = False

# if not os.path.isdir('./data/'):
#     os.makedirs('./data/')

# if not os.path.isdir('./temp'):
#     os.makedirs('./temp/')

# # Adjusting images to be centralized.
# with open("style.css") as f:
#     st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    
# def get_binary_file_downloader_html(bin_file, file_label='File'):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     bin_str = base64.b64encode(data).decode()
#     href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
#     return href
    
# if __name__ == "__main__":

    
#     state = get_state()

#     st.title('DICOM Viewer')

#     st.sidebar.title('DICOM Image Viewer')

#     demo_button = st.sidebar.checkbox('Demo', value=False, key='demo_checkbox')
    
#     url_input = st.sidebar.text_input('Enter the Google Drive shared url for the .dcm files', key='url_input')
    
#     st.sidebar.markdown('<h5>MAX FILE SIZE: 100 MB</h5>', unsafe_allow_html=True)
#     st.sidebar.markdown(' ')
#     st.sidebar.markdown('or')

#     file_uploaded =  st.sidebar.file_uploader("Upload a .zip with .dcm files (slower than GDrive)", type="zip", key='file_uploader')

#     if demo_button:
#         url_input = 'https://drive.google.com/file/d/1ESRZpJA92g8L4PqT2adCN3hseFbnw9Hg/view?usp=sharing'

#     if file_uploaded:
#         if not state[data_key]:
#             if does_zip_have_dcm(file_uploaded):
#                 store_data(file_uploaded)
#                 data_has_changed = True
    
#     if url_input:
#         if not state[data_key]:
#             if download_zip_from_url(url_input):
#                 data_has_changed = True

#     if st.sidebar.button('---------- Refresh input data ----------', key='refresh_button'):
#         clear_data_storage(temp_data_directory + get_report_ctx().session_id + '/')
#         clear_data_storage(temp_zip_folder)
#         st.caching.clear_cache()
#         url_input = st.empty()
#         data_is_ready = False
#         data_has_changed = False
#         state[data_key] = False
#         state.clear()

#     if data_has_changed:
#         valid_folders = get_DCM_valid_folders(temp_data_directory + get_report_ctx().session_id + '/')
        
#         for folder in valid_folders:
#             state[folder.split('/')[-1]] = ('', '', {'Anomaly': 'Bleeding', 'Slices': ''})

#         state[data_key] = True
#         state['valid_folders'] = valid_folders
#         state.last_serie = ''

#         data_has_changed = False
    
#     if state[data_key]:
#         data_is_ready = True
    
#     if data_is_ready:
#         series_names = get_series_names(state['valid_folders'])
        
#         selected_serie = st.selectbox('Select a series', series_names, index=0, key='select_series')

#         st.markdown('<h2>Patient Info</h2>', unsafe_allow_html=True)
#         display_info = st.checkbox('Display data', value=True)

#         if state.last_serie != selected_serie:
#             st.caching.clear_cache()
#             state.last_serie = selected_serie

#         img3d, info = processing_data(state['valid_folders'][series_names.index(selected_serie)] + '/')
            
#         if display_info:
#             st.dataframe(info)

        
#         slice_slider = st.slider(
#             'Slices',
#             0, img3d.shape[2] - 1, (img3d.shape[2] - 1)//2,
#             key='slice_slider'
#         )

#         color_threshold = st.slider(
#             'Color Threshold',
#             0, 100, 50,
#             key='color_threshold_slider'
#         )
#         def rotate_and_resize(image, angle, size):
#             rotated = ndimage.rotate(image, angle)
#             resized = resize(rotated, size)
#             return resized

#         axial_max = int(img3d[:, :, slice_slider].max())
#         axial_threshold = axial_max * ((2 * color_threshold / 100) - 1)
#         axial_slice = normalize_image(filter_image(axial_threshold, img3d[:, :, slice_slider]))

#         coronal_max = int(img3d[slice_slider, :, :].max())
#         coronal_threshold = coronal_max * ((2 * color_threshold / 100) - 1)
#         coronal_slice = normalize_image(filter_image(coronal_threshold, rotate_and_resize(img3d[slice_slider, :, :]
# , 90, (img3d.shape[0], img3d.shape[0]))))

#         sagittal_max = int(img3d[:, slice_slider, :].max())
#         sagittal_threshold = sagittal_max * ((2 * color_threshold / 100) - 1)
#         sagittal_slice = normalize_image(filter_image(sagittal_threshold, rotate_and_resize(img3d[:, slice_slider, :]
# , 90, (img3d.shape[0], img3d.shape[0]))))

#         #  Display the slices horizontally
#         st.image([axial_slice, coronal_slice, sagittal_slice], caption=['Axial Slice {}'.format(slice_slider), 'Coronal Slice {}'.format(slice_slider), 'Sagittal Slice {}'.format(slice_slider)], width=width)
        
#         st.sidebar.markdown('<h1 style=\'font-size:0.65em\'> Example of annotation with slices: 0-11; 57-59; 112; </h1> ', unsafe_allow_html=True)

#         state[selected_serie][2]['Anomaly'] = st.sidebar.text_input('Anomaly Label', value=state[selected_serie][2]['Anomaly'], key='anomaly_label')

#         state[selected_serie][2]['Slices'] = st.sidebar.text_input("Axial Annotation - Slices with Anomaly", value=state[selected_serie][2]['Slices'], key='axial_annotation_input')

#         annotation_selected = st.sidebar.multiselect('Annotated series to be included in the .json', series_names, series_names, key='annotation_multiselect')
#         json_selected = {serie: state[serie][2] for serie in annotation_selected}
        
#         if st.checkbox('Check Annotations.json', value=True):
#             st.write(json_selected)
        
#         download_button_str = download_button(json_selected, 'Annotation.json', 'Download Annotation.json')
#         st.sidebar.markdown(download_button_str, unsafe_allow_html=True) 

#         # Export button for JSON data
#         if st.sidebar.button('Export Annotations as JSON'):
#             with open('Annotation.json', 'w') as json_file:
#                 json.dump(json_selected, json_file)
#             st.sidebar.markdown(get_binary_file_downloader_html('Annotation.json', 'JSON'), unsafe_allow_html=True)

#         # Export button for Images
#         if st.sidebar.button('Export Images'):
#             # Save the axial, coronal, and sagittal slices as image files
#             with zipfile.ZipFile('DICOM_Slices.zip', 'w') as zipf:
#                 # Save the axial slice as an image file
#                 axial_slice_filename = 'Axial_Slice_{}.dcm'.format(slice_slider)
#                 axial_slice_path = os.path.join('./', axial_slice_filename)
#                 st.image(axial_slice, caption='Axial Slice', use_column_width=True)
#                 st.write('Downloading Axial Slice as:', axial_slice_filename)
#                 with open(axial_slice_path, 'wb') as f:
#                     f.write(axial_slice)
#                 zipf.write(axial_slice_path, os.path.basename(axial_slice_path))

#                 # Save the coronal slice as an image file
#                 coronal_slice_filename = 'Coronal_Slice_{}.png'.format(slice_slider)
#                 coronal_slice_path = os.path.join('./', coronal_slice_filename)
#                 st.image(coronal_slice, caption='Coronal Slice', use_column_width=True)
#                 st.write('Downloading Coronal Slice as:', coronal_slice_filename)
#                 with open(coronal_slice_path, 'wb') as f:
#                     f.write(coronal_slice)
#                 zipf.write(coronal_slice_path, os.path.basename(coronal_slice_path))

#                 # Save the sagittal slice as an image file
#                 sagittal_slice_filename = 'Sagittal_Slice_{}.png'.format(slice_slider)
#                 sagittal_slice_path = os.path.join('./', sagittal_slice_filename)
#                 st.image(sagittal_slice, caption='Sagittal Slice', use_column_width=True)
#                 st.write('Downloading Sagittal Slice as:', sagittal_slice_filename)
#                 with open(sagittal_slice_path, 'wb') as f:
#                     f.write(sagittal_slice)
#                 zipf.write(sagittal_slice_path, os.path.basename(sagittal_slice_path))

#             st.markdown(get_binary_file_downloader_html('DICOM_Slices.zip', 'DICOM Slices'), unsafe_allow_html=True)
     
#         del img3d, info

#     if st.sidebar.checkbox('Notes'):
#         st.sidebar.markdown('1. It does not recognize zip folders inside other zip folders.')
#         st.sidebar.markdown('2. It only recognizes series with two or more .dcm files.')
#         st.sidebar.markdown('3. You can use the arrow keys to change the slider widgets.')
#         st.sidebar.markdown('3. Uploaded files are cached until the heroku session becomes idle (30 min).'
#                             ' Then, they are automatically deleted.')
#         st.sidebar.markdown('4. If you want to manually reset/delete previously uploaded data via URL, ' 
#                             'clear the text input, and press the button to refresh input data. '
#                             'In case you are using the File Uploader widget, perform the same '
#                             'actions described above and then refresh the page with F5. ')
    
#     gc.collect()
#     state.sync()
####################################################separate dcm file getting####################################################
# import streamlit as st
# from src.utils import *
# import gc
# import numpy as np
# from scipy import ndimage
# from skimage.transform import resize
# import json
# import os
# import base64

# # Hide FileUploader deprecation
# st.set_option('deprecation.showfileUploaderEncoding', False)

# # Hide streamlit header
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """

# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# data_key = 'has_data'
# width = 400
# data_is_ready = False
# data_has_changed = False

# if not os.path.isdir('./data/'):
#     os.makedirs('./data/')

# if not os.path.isdir('./temp'):
#     os.makedirs('./temp/')

# # Adjusting images to be centralized.
# with open("style.css") as f:
#     st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    
# def get_binary_file_downloader_html(bin_file, file_label='File'):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     bin_str = base64.b64encode(data).decode()
#     href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
#     return href
    
# if __name__ == "__main__":

    
#     state = get_state()

#     st.title('DICOM Viewer')

#     st.sidebar.title('DICOM Image Viewer')

#     demo_button = st.sidebar.checkbox('Demo', value=False, key='demo_checkbox')
    
#     url_input = st.sidebar.text_input('Enter the Google Drive shared url for the .dcm files', key='url_input')
    
#     st.sidebar.markdown('<h5>MAX FILE SIZE: 100 MB</h5>', unsafe_allow_html=True)
#     st.sidebar.markdown(' ')
#     st.sidebar.markdown('or')

#     file_uploaded =  st.sidebar.file_uploader("Upload a .zip with .dcm files (slower than GDrive)", type="zip", key='file_uploader')

#     if demo_button:
#         url_input = 'https://drive.google.com/file/d/1ESRZpJA92g8L4PqT2adCN3hseFbnw9Hg/view?usp=sharing'

#     if file_uploaded:
#         if not state[data_key]:
#             if does_zip_have_dcm(file_uploaded):
#                 store_data(file_uploaded)
#                 data_has_changed = True
    
#     if url_input:
#         if not state[data_key]:
#             if download_zip_from_url(url_input):
#                 data_has_changed = True

#     if st.sidebar.button('---------- Refresh input data ----------', key='refresh_button'):
#         clear_data_storage(temp_data_directory + get_report_ctx().session_id + '/')
#         clear_data_storage(temp_zip_folder)
#         st.caching.clear_cache()
#         url_input = st.empty()
#         data_is_ready = False
#         data_has_changed = False
#         state[data_key] = False
#         state.clear()

#     if data_has_changed:
#         valid_folders = get_DCM_valid_folders(temp_data_directory + get_report_ctx().session_id + '/')
        
#         for folder in valid_folders:
#             state[folder.split('/')[-1]] = ('', '', {'Anomaly': 'Bleeding', 'Slices': ''})

#         state[data_key] = True
#         state['valid_folders'] = valid_folders
#         state.last_serie = ''

#         data_has_changed = False
    
#     if state[data_key]:
#         data_is_ready = True
    
#     if data_is_ready:
#         series_names = get_series_names(state['valid_folders'])
        
#         selected_serie = st.selectbox('Select a series', series_names, index=0, key='select_series')

#         st.markdown('<h2>Patient Info</h2>', unsafe_allow_html=True)
#         display_info = st.checkbox('Display data', value=True)

#         if state.last_serie != selected_serie:
#             st.caching.clear_cache()
#             state.last_serie = selected_serie

#         if selected_serie in series_names:
#             img3d, info = processing_data(state['valid_folders'][series_names.index(selected_serie)] + '/')
            
#             if display_info:
#                 st.dataframe(info)

            
#             slice_slider = st.slider(
#                 'Slices',
#                 0, img3d.shape[2] - 1, (img3d.shape[2] - 1)//2,
#                 key='slice_slider'
#             )

#             color_threshold = st.slider(
#                 'Color Threshold',
#                 0, 100, 50,
#                 key='color_threshold_slider'
#             )
#             def rotate_and_resize(image, angle, size):
#                 rotated = ndimage.rotate(image, angle)
#                 resized = resize(rotated, size)
#                 return resized

#             axial_max = int(img3d[:, :, slice_slider].max())
#             axial_threshold = axial_max * ((2 * color_threshold / 100) - 1)
#             axial_slice = normalize_image(filter_image(axial_threshold, img3d[:, :, slice_slider]))

#             coronal_max = int(img3d[slice_slider, :, :].max())
#             coronal_threshold = coronal_max * ((2 * color_threshold / 100) - 1)
#             coronal_slice = normalize_image(filter_image(coronal_threshold, rotate_and_resize(img3d[slice_slider, :, :]
#     , 90, (img3d.shape[0], img3d.shape[0]))))

#             sagittal_max = int(img3d[:, slice_slider, :].max())
#             sagittal_threshold = sagittal_max * ((2 * color_threshold / 100) - 1)
#             sagittal_slice = normalize_image(filter_image(sagittal_threshold, rotate_and_resize(img3d[:, slice_slider, :]
#     , 90, (img3d.shape[0], img3d.shape[0]))))

#             #  Display the slices horizontally
#             st.image([axial_slice, coronal_slice, sagittal_slice], caption=['Axial Slice {}'.format(slice_slider), 'Coronal Slice {}'.format(slice_slider), 'Sagittal Slice {}'.format(slice_slider)], width=width)
            
#             st.sidebar.markdown('<h1 style=\'font-size:0.65em\'> Example of annotation with slices: 0-11; 57-59; 112; </h1> ', unsafe_allow_html=True)

#             state[selected_serie][2]['Anomaly'] = st.sidebar.text_input('Anomaly Label', value=state[selected_serie][2]['Anomaly'], key='anomaly_label')

#             state[selected_serie][2]['Slices'] = st.sidebar.text_input("Axial Annotation - Slices with Anomaly", value=state[selected_serie][2]['Slices'], key='axial_annotation_input')

#             annotation_selected = st.sidebar.multiselect('Annotated series to be included in the .json', series_names, series_names, key='annotation_multiselect')
#             json_selected = {serie: state[serie][2] for serie in annotation_selected}
            
#             if st.checkbox('Check Annotations.json', value=True):
#                 st.write(json_selected)
            
#             download_button_str = download_button(json_selected, 'Annotation.json', 'Download Annotation.json')
#             st.sidebar.markdown(download_button_str, unsafe_allow_html=True) 

#             # Export button for JSON data
#             if st.sidebar.button('Export Annotations as JSON'):
#                 with open('Annotation.json', 'w') as json_file:
#                     json.dump(json_selected, json_file)
#                 st.sidebar.markdown(get_binary_file_downloader_html('Annotation.json', 'JSON'), unsafe_allow_html=True)

#             # Export button for Images
#             if st.sidebar.button('Export Images'):
#                 # Save the axial slice as an image file
#                 axial_slice_filename = 'Axial_Slice_{}.dcm'.format(slice_slider)
#                 axial_slice_path = os.path.join('./', axial_slice_filename)
#                 st.image(axial_slice, caption='Axial Slice', use_column_width=True)
#                 st.write('Downloading Axial Slice as:', axial_slice_filename)
#                 with open(axial_slice_path, 'wb') as f:
#                     f.write(axial_slice)

#                 # Save the coronal slice as an image file
#                 coronal_slice_filename = 'Coronal_Slice_{}.dcm'.format(slice_slider)
#                 coronal_slice_path = os.path.join('./', coronal_slice_filename)
#                 st.image(coronal_slice, caption='Coronal Slice', use_column_width=True)
#                 st.write('Downloading Coronal Slice as:', coronal_slice_filename)
#                 with open(coronal_slice_path, 'wb') as f:
#                     f.write(coronal_slice)

#                 # Save the sagittal slice as an image file
#                 sagittal_slice_filename = 'Sagittal_Slice_{}.dcm'.format(slice_slider)
#                 sagittal_slice_path = os.path.join('./', sagittal_slice_filename)
#                 st.image(sagittal_slice, caption='Sagittal Slice', use_column_width=True)
#                 st.write('Downloading Sagittal Slice as:', sagittal_slice_filename)
#                 with open(sagittal_slice_path, 'wb') as f:
#                     f.write(sagittal_slice)

#                 st.markdown(get_binary_file_downloader_html(axial_slice_path, 'Axial Slice'), unsafe_allow_html=True)
#                 st.markdown(get_binary_file_downloader_html(coronal_slice_path, 'Coronal Slice'), unsafe_allow_html=True)
#                 st.markdown(get_binary_file_downloader_html(sagittal_slice_path, 'Sagittal Slice'), unsafe_allow_html=True)
         
#             del img3d, info
#         else:
#             st.warning("Selected series not found. Please choose a valid series.")

#     if st.sidebar.checkbox('Notes'):
#         st.sidebar.markdown('1. It does not recognize zip folders inside other zip folders.')
#         st.sidebar.markdown('2. It only recognizes series with two or more .dcm files.')
#         st.sidebar.markdown('3. You can use the arrow keys to change the slider widgets.')
#         st.sidebar.markdown('3. Uploaded files are cached until the heroku session becomes idle (30 min).'
#                             ' Then, they are automatically deleted.')
#         st.sidebar.markdown('4. If you want to manually reset/delete previously uploaded data via URL, ' 
#                             'clear the text input, and press the button to refresh input data. '
#                             'In case you are using the File Uploader widget, perform the same '
#                             'actions described above and then refresh the page with F5. ')
    
#     gc.collect()
#     state.sync()
#####################3+all download file ########################
# import streamlit as st
# from src.utils import *
# import gc
# import numpy as np
# from scipy import ndimage
# from skimage.transform import resize
# import json
# import os
# import base64
# import zipfile

# # Hide FileUploader deprecation
# st.set_option('deprecation.showfileUploaderEncoding', False)

# # Hide streamlit header
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """

# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# data_key = 'has_data'
# width = 400
# data_is_ready = False
# data_has_changed = False

# if not os.path.isdir('./data/'):
#     os.makedirs('./data/')

# if not os.path.isdir('./temp'):
#     os.makedirs('./temp/')

# # Adjusting images to be centralized.
# with open("style.css") as f:
#     st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    
# def get_binary_file_downloader_html(bin_file, file_label='File'):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     bin_str = base64.b64encode(data).decode()
#     href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
#     return href
    
# if __name__ == "__main__":

#     state = get_state()

#     st.title('DICOM Viewer')

#     st.sidebar.title('DICOM Image Viewer')

#     demo_button = st.sidebar.checkbox('Demo', value=False, key='demo_checkbox')
    
#     url_input = st.sidebar.text_input('Enter the Google Drive shared url for the .dcm files', key='url_input')
    
#     st.sidebar.markdown('<h5>MAX FILE SIZE: 100 MB</h5>', unsafe_allow_html=True)
#     st.sidebar.markdown(' ')
#     st.sidebar.markdown('or')

#     file_uploaded =  st.sidebar.file_uploader("Upload a .zip with .dcm files (slower than GDrive)", type="zip", key='file_uploader')

#     if demo_button:
#         url_input = 'https://drive.google.com/file/d/1ESRZpJA92g8L4PqT2adCN3hseFbnw9Hg/view?usp=sharing'

#     if file_uploaded:
#         if not state[data_key]:
#             if does_zip_have_dcm(file_uploaded):
#                 store_data(file_uploaded)
#                 data_has_changed = True
    
#     if url_input:
#         if not state[data_key]:
#             if download_zip_from_url(url_input):
#                 data_has_changed = True

#     if st.sidebar.button('---------- Refresh input data ----------', key='refresh_button'):
#         clear_data_storage(temp_data_directory + get_report_ctx().session_id + '/')
#         clear_data_storage(temp_zip_folder)
#         st.caching.clear_cache()
#         url_input = st.empty()
#         data_is_ready = False
#         data_has_changed = False
#         state[data_key] = False
#         state.clear()

#     if data_has_changed:
#         valid_folders = get_DCM_valid_folders(temp_data_directory + get_report_ctx().session_id + '/')
        
#         for folder in valid_folders:
#             state[folder.split('/')[-1]] = ('', '', {'Anomaly': 'Bleeding', 'Slices': ''})

#         state[data_key] = True
#         state['valid_folders'] = valid_folders
#         state.last_serie = ''

#         data_has_changed = False
    
#     if state[data_key]:
#         data_is_ready = True
    
#     if data_is_ready:
#         series_names = get_series_names(state['valid_folders'])
        
#         selected_serie = st.selectbox('Select a series', series_names, index=0, key='select_series')

#         st.markdown('<h2>Patient Info</h2>', unsafe_allow_html=True)
#         display_info = st.checkbox('Display data', value=True)

#         if state.last_serie != selected_serie:
#             st.caching.clear_cache()
#             state.last_serie = selected_serie

#         if selected_serie in series_names:
#             img3d, info = processing_data(state['valid_folders'][series_names.index(selected_serie)] + '/')
            
#             if display_info:
#                 st.dataframe(info)

            
#             slice_slider = st.slider(
#                 'Slices',
#                 0, img3d.shape[2] - 1, (img3d.shape[2] - 1)//2,
#                 key='slice_slider'
#             )

#             color_threshold = st.slider(
#                 'Color Threshold',
#                 0, 100, 50,
#                 key='color_threshold_slider'
#             )
#             def rotate_and_resize(image, angle, size):
#                 rotated = ndimage.rotate(image, angle)
#                 resized = resize(rotated, size)
#                 return resized

#             axial_max = int(img3d[:, :, slice_slider].max())
#             axial_threshold = axial_max * ((2 * color_threshold / 100) - 1)
#             axial_slice = normalize_image(filter_image(axial_threshold, img3d[:, :, slice_slider]))

#             coronal_max = int(img3d[slice_slider, :, :].max())
#             coronal_threshold = coronal_max * ((2 * color_threshold / 100) - 1)
#             coronal_slice = normalize_image(filter_image(coronal_threshold, rotate_and_resize(img3d[slice_slider, :, :]
#     , 90, (img3d.shape[0], img3d.shape[0]))))

#             sagittal_max = int(img3d[:, slice_slider, :].max())
#             sagittal_threshold = sagittal_max * ((2 * color_threshold / 100) - 1)
#             sagittal_slice = normalize_image(filter_image(sagittal_threshold, rotate_and_resize(img3d[:, slice_slider, :]
#     , 90, (img3d.shape[0], img3d.shape[0]))))

#             #  Display the slices horizontally
#             st.image([axial_slice, coronal_slice, sagittal_slice], caption=['Axial Slice {}'.format(slice_slider), 'Coronal Slice {}'.format(slice_slider), 'Sagittal Slice {}'.format(slice_slider)], width=width)
            
#             st.sidebar.markdown('<h1 style=\'font-size:0.65em\'> Example of annotation with slices: 0-11; 57-59; 112; </h1> ', unsafe_allow_html=True)

#             state[selected_serie][2]['Anomaly'] = st.sidebar.text_input('Anomaly Label', value=state[selected_serie][2]['Anomaly'], key='anomaly_label')

#             state[selected_serie][2]['Slices'] = st.sidebar.text_input("Axial Annotation - Slices with Anomaly", value=state[selected_serie][2]['Slices'], key='axial_annotation_input')

#             annotation_selected = st.sidebar.multiselect('Annotated series to be included in the .json', series_names, series_names, key='annotation_multiselect')
#             json_selected = {serie: state[serie][2] for serie in annotation_selected}
            
#             if st.checkbox('Check Annotations.json', value=True):
#                 st.write(json_selected)
            
#             download_button_str = download_button(json_selected, 'Annotation.json', 'Download Annotation.json')
#             st.sidebar.markdown(download_button_str, unsafe_allow_html=True) 

#             # Export button for JSON data
#             if st.sidebar.button('Export Annotations as JSON'):
#                 with open('Annotation.json', 'w') as json_file:
#                     json.dump(json_selected, json_file)
#                 st.sidebar.markdown(get_binary_file_downloader_html('Annotation.json', 'JSON'), unsafe_allow_html=True)

#             # Export button for Images
#             if st.sidebar.button('Export Images'):
#                 # Save the axial slice as an image file
#                 axial_slice_filename = 'Axial_Slice_{}.dcm'.format(slice_slider)
#                 axial_slice_path = os.path.join('./temp/', axial_slice_filename)
#                 with open(axial_slice_path, 'wb') as f:
#                     f.write(axial_slice)

#                 # Save the coronal slice as an image file
#                 coronal_slice_filename = 'Coronal_Slice_{}.dcm'.format(slice_slider)
#                 coronal_slice_path = os.path.join('./temp/', coronal_slice_filename)
#                 with open(coronal_slice_path, 'wb') as f:
#                     f.write(coronal_slice)

#                 # Save the sagittal slice as an image file
#                 sagittal_slice_filename = 'Sagittal_Slice_{}.dcm'.format(slice_slider)
#                 sagittal_slice_path = os.path.join('./temp/', sagittal_slice_filename)
#                 with open(sagittal_slice_path, 'wb') as f:
#                     f.write(sagittal_slice)

#                 st.markdown(get_binary_file_downloader_html(axial_slice_path, 'Axial Slice'), unsafe_allow_html=True)
#                 st.markdown(get_binary_file_downloader_html(coronal_slice_path, 'Coronal Slice'), unsafe_allow_html=True)
#                 st.markdown(get_binary_file_downloader_html(sagittal_slice_path, 'Sagittal Slice'), unsafe_allow_html=True)

#                 # Create a zip file containing all three slices
#                 zip_filename = 'DICOM_Slices.zip'
#                 with zipfile.ZipFile(zip_filename, 'w') as zipf:
#                     zipf.write(axial_slice_path, os.path.basename(axial_slice_path))
#                     zipf.write(coronal_slice_path, os.path.basename(coronal_slice_path))
#                     zipf.write(sagittal_slice_path, os.path.basename(sagittal_slice_path))

#                 # Provide a download link for the zip file
#                 st.markdown(get_binary_file_downloader_html(zip_filename, 'Download All Slices'), unsafe_allow_html=True)
         
#             del img3d, info
#         else:
#             st.warning("Selected series not found. Please choose a valid series.")

#     if st.sidebar.checkbox('Notes'):
#         st.sidebar.markdown('1. It does not recognize zip folders inside other zip folders.')
#         st.sidebar.markdown('2. It only recognizes series with two or more .dcm files.')
#         st.sidebar.markdown('3. You can use the arrow keys to change the slider widgets.')
#         st.sidebar.markdown('3. Uploaded files are cached until the heroku session becomes idle (30 min).'
#                             ' Then, they are automatically deleted.')
#         st.sidebar.markdown('4. If you want to manually reset/delete previously uploaded data via URL, ' 
#                             'clear the text input, and press the button to refresh input data. '
#                             'In case you are using the File Uploader widget, perform the same '
#                             'actions described above and then refresh the page with F5. ')
    
#     gc.collect()
#     state.sync()
##########working 
import streamlit as st
from src.utils import *
import gc
import numpy as np
from scipy import ndimage
from skimage.transform import resize
import json
import os
import base64
import zipfile

# Hide FileUploader deprecation
st.set_option('deprecation.showfileUploaderEncoding', False)

# Hide streamlit header
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

data_key = 'has_data'
width = 400
data_is_ready = False
data_has_changed = False

if not os.path.isdir('./data/'):
    os.makedirs('./data/')

if not os.path.isdir('./temp'):
    os.makedirs('./temp/')

# Adjusting images to be centralized.
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
    return href
    
if __name__ == "__main__":

    state = get_state()

    st.title('DICOM Viewer')

    st.sidebar.title('DICOM Image Viewer')

    demo_button = st.sidebar.checkbox('Demo', value=False, key='demo_checkbox')
    
    url_input = st.sidebar.text_input('Enter the Google Drive shared url for the .dcm files', key='url_input')
    
    st.sidebar.markdown('<h5>MAX FILE SIZE: 100 MB</h5>', unsafe_allow_html=True)
    st.sidebar.markdown(' ')
    st.sidebar.markdown('or')

    file_uploaded =  st.sidebar.file_uploader("Upload a .zip with .dcm files (slower than GDrive)", type="zip", key='file_uploader')

    if demo_button:
        url_input = 'https://drive.google.com/file/d/1ESRZpJA92g8L4PqT2adCN3hseFbnw9Hg/view?usp=sharing'

    if file_uploaded:
        if not state[data_key]:
            if does_zip_have_dcm(file_uploaded):
                store_data(file_uploaded)
                data_has_changed = True
    
    if url_input:
        if not state[data_key]:
            if download_zip_from_url(url_input):
                data_has_changed = True

    if st.sidebar.button('---------- Refresh input data ----------', key='refresh_button'):
        clear_data_storage(temp_data_directory + get_report_ctx().session_id + '/')
        clear_data_storage(temp_zip_folder)
        st.caching.clear_cache()
        url_input = st.empty()
        data_is_ready = False
        data_has_changed = False
        state[data_key] = False
        state.clear()

    if data_has_changed:
        valid_folders = get_DCM_valid_folders(temp_data_directory + get_report_ctx().session_id + '/')
        
        for folder in valid_folders:
            state[folder.split('/')[-1]] = ('', '', {'Anomaly': 'Bleeding', 'Slices': ''})

        state[data_key] = True
        state['valid_folders'] = valid_folders
        state.last_serie = ''

        data_has_changed = False
    
    if state[data_key]:
        data_is_ready = True
    
    if data_is_ready:
        series_names = get_series_names(state['valid_folders'])
        
        selected_serie = st.selectbox('Select a series', series_names, index=0, key='select_series')

        st.markdown('<h2>Patient Info</h2>', unsafe_allow_html=True)
        display_info = st.checkbox('Display data', value=True)

        if state.last_serie != selected_serie:
            st.caching.clear_cache()
            state.last_serie = selected_serie

        if selected_serie in series_names:
            img3d, info = processing_data(state['valid_folders'][series_names.index(selected_serie)] + '/')
            
            if display_info:
                st.dataframe(info)

            
            slice_slider = st.slider(
                'Slices',
                0, img3d.shape[2] - 1, (img3d.shape[2] - 1)//2,
                key='slice_slider'
            )

            color_threshold = st.slider(
                'Color Threshold',
                0, 100, 50,
                key='color_threshold_slider'
            )
            def rotate_and_resize(image, angle, size):
                rotated = ndimage.rotate(image, angle)
                resized = resize(rotated, size)
                return resized

            axial_max = int(img3d[:, :, slice_slider].max())
            axial_threshold = axial_max * ((2 * color_threshold / 100) - 1)
            axial_slice = normalize_image(filter_image(axial_threshold, img3d[:, :, slice_slider]))

            coronal_max = int(img3d[slice_slider, :, :].max())
            coronal_threshold = coronal_max * ((2 * color_threshold / 100) - 1)
            coronal_slice = normalize_image(filter_image(coronal_threshold, rotate_and_resize(img3d[slice_slider, :, :]
    , 90, (img3d.shape[0], img3d.shape[0]))))

            sagittal_max = int(img3d[:, slice_slider, :].max())
            sagittal_threshold = sagittal_max * ((2 * color_threshold / 100) - 1)
            sagittal_slice = normalize_image(filter_image(sagittal_threshold, rotate_and_resize(img3d[:, slice_slider, :]
    , 90, (img3d.shape[0], img3d.shape[0]))))

            #  Display the slices horizontally
            st.image([axial_slice, coronal_slice, sagittal_slice], caption=['Axial Slice {}'.format(slice_slider), 'Coronal Slice {}'.format(slice_slider), 'Sagittal Slice {}'.format(slice_slider)], width=width)
            
            st.sidebar.markdown('<h1 style=\'font-size:0.65em\'> Example of annotation with slices: 0-11; 57-59; 112; </h1> ', unsafe_allow_html=True)

            state[selected_serie][2]['Anomaly'] = st.sidebar.text_input('Anomaly Label', value=state[selected_serie][2]['Anomaly'], key='anomaly_label')

            state[selected_serie][2]['Slices'] = st.sidebar.text_input("Axial Annotation - Slices with Anomaly", value=state[selected_serie][2]['Slices'], key='axial_annotation_input')

            annotation_selected = st.sidebar.multiselect('Annotated series to be included in the .json', series_names, series_names, key='annotation_multiselect')
            json_selected = {serie: state[serie][2] for serie in annotation_selected}
            
            if st.checkbox('Check Annotations.json', value=True):
                st.write(json_selected)
            
            download_button_str = download_button(json_selected, 'Annotation.json', 'Download Annotation.json')
            st.sidebar.markdown(download_button_str, unsafe_allow_html=True) 

            # Export button for JSON data
            if st.sidebar.button('Export Annotations as JSON'):
                with open('Annotation.json', 'w') as json_file:
                    json.dump(json_selected, json_file)
                st.sidebar.markdown(get_binary_file_downloader_html('Annotation.json', 'JSON'), unsafe_allow_html=True)

            # Export button for Images
            if st.sidebar.button('Export Images'):
                # Save the axial slice as an image file
                axial_slice_filename = 'Axial_Slice_{}.dcm'.format(slice_slider)
                axial_slice_path = os.path.join('./temp/', axial_slice_filename)
                with open(axial_slice_path, 'wb') as f:
                    f.write(axial_slice)

                # Save the coronal slice as an image file
                coronal_slice_filename = 'Coronal_Slice_{}.dcm'.format(slice_slider)
                coronal_slice_path = os.path.join('./temp/', coronal_slice_filename)
                with open(coronal_slice_path, 'wb') as f:
                    f.write(coronal_slice)

                # Save the sagittal slice as an image file
                sagittal_slice_filename = 'Sagittal_Slice_{}.dcm'.format(slice_slider)
                sagittal_slice_path = os.path.join('./temp/', sagittal_slice_filename)
                with open(sagittal_slice_path, 'wb') as f:
                    f.write(sagittal_slice)

                st.markdown(get_binary_file_downloader_html(axial_slice_path, 'Axial Slice'), unsafe_allow_html=True)
                st.markdown(get_binary_file_downloader_html(coronal_slice_path, 'Coronal Slice'), unsafe_allow_html=True)
                st.markdown(get_binary_file_downloader_html(sagittal_slice_path, 'Sagittal Slice'), unsafe_allow_html=True)

                # Create a zip file containing all three slices
                zip_filename = 'DICOM_Slices.zip'
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    zipf.write(axial_slice_path, os.path.basename(axial_slice_path))
                    zipf.write(coronal_slice_path, os.path.basename(coronal_slice_path))
                    zipf.write(sagittal_slice_path, os.path.basename(sagittal_slice_path))

                # Provide a download link for the zip file
                st.markdown(get_binary_file_downloader_html(zip_filename, 'Download All Slices'), unsafe_allow_html=True)
         
            del img3d, info
        else:
            st.warning("Selected series not found. Please choose a valid series.")

    if st.sidebar.checkbox('Notes'):
        st.sidebar.markdown('1. It does not recognize zip folders inside other zip folders.')
        st.sidebar.markdown('2. It only recognizes series with two or more .dcm files.')
        st.sidebar.markdown('3. You can use the arrow keys to change the slider widgets.')
        st.sidebar.markdown('3. Uploaded files are cached until the heroku session becomes idle (30 min).'
                            ' Then, they are automatically deleted.')
        st.sidebar.markdown('4. If you want to manually reset/delete previously uploaded data via URL, ' 
                            'clear the text input, and press the button to refresh input data. '
                            'In case you are using the File Uploader widget, perform the same '
                            'actions described above and then refresh the page with F5. ')
    
    gc.collect()
    state.sync()
# ######
# import streamlit as st
# import pydicom
# import numpy as np
# from PIL import Image, ImageDraw
# from src.utils import *
# import gc
# from scipy import ndimage
# from skimage.transform import resize
# import json
# import os
# import base64
# import zipfile

# # Function to annotate DICOM images
# def annotate_image(image_array, annotations):
#     image = Image.fromarray(image_array)
#     draw = ImageDraw.Draw(image)
#     for annotation in annotations:
#         draw.rectangle(annotation, outline='red')
#     return image

# # Hide FileUploader deprecation
# st.set_option('deprecation.showfileUploaderEncoding', False)

# # Hide Streamlit header and footer
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# # Initialize variables
# data_key = 'has_data'
# width = 400
# data_is_ready = False
# data_has_changed = False

# # Create necessary directories
# if not os.path.isdir('./data/'):
#     os.makedirs('./data/')

# if not os.path.isdir('./temp'):
#     os.makedirs('./temp/')

# # Adjust images to be centralized
# with open("style.css") as f:
#     st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# def get_binary_file_downloader_html(bin_file, file_label='File'):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     bin_str = base64.b64encode(data).decode()
#     href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
#     return href

# if __name__ == "__main__":
#     state = get_state()

#     st.title('DICOM Viewer with Annotation')

#     st.sidebar.title('DICOM Image Viewer')

#     demo_button = st.sidebar.checkbox('Demo', value=False, key='demo_checkbox')
    
#     url_input = st.sidebar.text_input('Enter the Google Drive shared url for the .dcm files', key='url_input')
    
#     st.sidebar.markdown('<h5>MAX FILE SIZE: 100 MB</h5>', unsafe_allow_html=True)
#     st.sidebar.markdown(' ')
#     st.sidebar.markdown('or')

#     file_uploaded =  st.sidebar.file_uploader("Upload a .zip with .dcm files (slower than GDrive)", type="zip", key='file_uploader')

#     if demo_button:
#         url_input = 'https://drive.google.com/file/d/1ESRZpJA92g8L4PqT2adCN3hseFbnw9Hg/view?usp=sharing'

#     if file_uploaded:
#         if not state[data_key]:
#             if does_zip_have_dcm(file_uploaded):
#                 store_data(file_uploaded)
#                 data_has_changed = True
    
#     if url_input:
#         if not state[data_key]:
#             if download_zip_from_url(url_input):
#                 data_has_changed = True

#     if st.sidebar.button('---------- Refresh input data ----------', key='refresh_button'):
#         clear_data_storage(temp_data_directory + get_report_ctx().session_id + '/')
#         clear_data_storage(temp_zip_folder)
#         st.caching.clear_cache()
#         url_input = st.empty()
#         data_is_ready = False
#         data_has_changed = False
#         state[data_key] = False
#         state.clear()

#     if data_has_changed:
#         valid_folders = get_DCM_valid_folders(temp_data_directory + get_report_ctx().session_id + '/')
        
#         for folder in valid_folders:
#             state[folder.split('/')[-1]] = ('', '', {'Anomaly': 'Bleeding', 'Slices': ''})

#         state[data_key] = True
#         state['valid_folders'] = valid_folders
#         state.last_serie = ''

#         data_has_changed = False
    
#     if state[data_key]:
#         data_is_ready = True
    
#     if data_is_ready:
#         series_names = get_series_names(state['valid_folders'])
        
#         selected_serie = st.selectbox('Select a series', series_names, index=0, key='select_series')

#         st.markdown('<h2>Patient Info</h2>', unsafe_allow_html=True)
#         display_info = st.checkbox('Display data', value=True)

#         if state.last_serie != selected_serie:
#             st.caching.clear_cache()
#             state.last_serie = selected_serie

#         if selected_serie in series_names:
#             img3d, info = processing_data(state['valid_folders'][series_names.index(selected_serie)] + '/')
            
#             if display_info:
#                 st.dataframe(info)

            
#             slice_slider = st.slider(
#                 'Slices',
#                 0, img3d.shape[2] - 1, (img3d.shape[2] - 1)//2,
#                 key='slice_slider'
#             )

#             color_threshold = st.slider(
#                 'Color Threshold',
#                 0, 100, 50,
#                 key='color_threshold_slider'
#             )
#             def rotate_and_resize(image, angle, size):
#                 rotated = ndimage.rotate(image, angle)
#                 resized = resize(rotated, size)
#                 return resized

#             axial_max = int(img3d[:, :, slice_slider].max())
#             axial_threshold = axial_max * ((2 * color_threshold / 100) - 1)
#             axial_slice = normalize_image(filter_image(axial_threshold, img3d[:, :, slice_slider]))

#             coronal_max = int(img3d[slice_slider, :, :].max())
#             coronal_threshold = coronal_max * ((2 * color_threshold / 100) - 1)
#             coronal_slice = normalize_image(filter_image(coronal_threshold, rotate_and_resize(img3d[slice_slider, :, :]
#     , 90, (img3d.shape[0], img3d.shape[0]))))

#             sagittal_max = int(img3d[:, slice_slider, :].max())
#             sagittal_threshold = sagittal_max * ((2 * color_threshold / 100) - 1)
#             sagittal_slice = normalize_image(filter_image(sagittal_threshold, rotate_and_resize(img3d[:, slice_slider, :]
#     , 90, (img3d.shape[0], img3d.shape[0]))))

#             #  Display the slices horizontally
#             st.image([axial_slice, coronal_slice, sagittal_slice], caption=['Axial Slice {}'.format(slice_slider), 'Coronal Slice {}'.format(slice_slider), 'Sagittal Slice {}'.format(slice_slider)], width=width)
            
#             st.sidebar.markdown('<h1 style=\'font-size:0.65em\'> Example of annotation with slices: 0-11; 57-59; 112; </h1> ', unsafe_allow_html=True)

#             state[selected_serie][2]['Anomaly'] = st.sidebar.text_input('Anomaly Label', value=state[selected_serie][2]['Anomaly'], key='anomaly_label')

#             state[selected_serie][2]['Slices'] = st.sidebar.text_input("Axial Annotation - Slices with Anomaly", value=state[selected_serie][2]['Slices'], key='axial_annotation_input')

#             annotation_selected = st.sidebar.multiselect('Annotated series to be included in the .json', series_names, series_names, key='annotation_multiselect')
#             json_selected = {serie: state[serie][2] for serie in annotation_selected}
            
#             if st.checkbox('Check Annotations.json', value=True):
#                 st.write(json_selected)
            
#             download_button_str = download_button(json_selected, 'Annotation.json', 'Download Annotation.json')
#             st.sidebar.markdown(download_button_str, unsafe_allow_html=True) 

#             # Export button for JSON data
#             if st.sidebar.button('Export Annotations as JSON'):
#                 with open('Annotation.json', 'w') as json_file:
#                     json.dump(json_selected, json_file)
#                 st.sidebar.markdown(get_binary_file_downloader_html('Annotation.json', 'JSON'), unsafe_allow_html=True)

#             # Export button for Images
#             if st.sidebar.button('Export Images'):
#                 # Save the axial slice as an image file
#                 axial_slice_filename = 'Axial_Slice_{}.dcm'.format(slice_slider)
#                 axial_slice_path = os.path.join('./temp/', axial_slice_filename)
#                 with open(axial_slice_path, 'wb') as f:
#                     f.write(axial_slice)

#                 # Save the coronal slice as an image file
#                 coronal_slice_filename = 'Coronal_Slice_{}.dcm'.format(slice_slider)
#                 coronal_slice_path = os.path.join('./temp/', coronal_slice_filename)
#                 with open(coronal_slice_path, 'wb') as f:
#                     f.write(coronal_slice)

#                 # Save the sagittal slice as an image file
#                 sagittal_slice_filename = 'Sagittal_Slice_{}.dcm'.format(slice_slider)
#                 sagittal_slice_path = os.path.join('./temp/', sagittal_slice_filename)
#                 with open(sagittal_slice_path, 'wb') as f:
#                     f.write(sagittal_slice)

#                 st.markdown(get_binary_file_downloader_html(axial_slice_path, 'Axial Slice'), unsafe_allow_html=True)
#                 st.markdown(get_binary_file_downloader_html(coronal_slice_path, 'Coronal Slice'), unsafe_allow_html=True)
#                 st.markdown(get_binary_file_downloader_html(sagittal_slice_path, 'Sagittal Slice'), unsafe_allow_html=True)

#                 # Create a zip file containing all three slices
#                 zip_filename = 'DICOM_Slices.zip'
#                 with zipfile.ZipFile(zip_filename, 'w') as zipf:
#                     zipf.write(axial_slice_path, os.path.basename(axial_slice_path))
#                     zipf.write(coronal_slice_path, os.path.basename(coronal_slice_path))
#                     zipf.write(sagittal_slice_path, os.path.basename(sagittal_slice_path))

#                 # Provide a download link for the zip file
#                 st.markdown(get_binary_file_downloader_html(zip_filename, 'Download All Slices'), unsafe_allow_html=True)
         
#             del img3d, info
#         else:
#             st.warning("Selected series not found. Please choose a valid series.")

#     if st.sidebar.checkbox('Notes'):
#         st.sidebar.markdown('1. It does not recognize zip folders inside other zip folders.')
#         st.sidebar.markdown('2. It only recognizes series with two or more .dcm files.')
#         st.sidebar.markdown('3. You can use the arrow keys to change the slider widgets.')
#         st.sidebar.markdown('3. Uploaded files are cached until the heroku session becomes idle (30 min).'
#                             ' Then, they are automatically deleted.')
#         st.sidebar.markdown('4. If you want to manually reset/delete previously uploaded data via URL, ' 
#                             'clear the text input, and press the button to refresh input data. '
#                             'In case you are using the File Uploader widget, perform the same '
#                             'actions described above and then refresh the page with F5. ')
    
#     gc.collect()
#     state.sync()
################################################
