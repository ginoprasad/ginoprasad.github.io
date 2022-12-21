#!/usr/bin/env python3
# coding: utf-8

# In[25]:


import os
import subprocess as sp
import yaml
import shutil


# # Convert notebooks to html

# In[26]:


metadata_path = 'metadata.yaml'


# In[27]:


with open(metadata_path) as infile:
    metadata = yaml.safe_load(infile)


# In[28]:


metadata


# In[29]:


temp_path = f'{os.getcwd()}/projects/temp.html'


# In[30]:


max_base_filename_length = 50


# In[31]:


project_names, project_paths = [], []
for project_notebook_path in metadata['Projects']:
    print(f"Converting {project_notebook_path}")
    sp.run(f"jupyter nbconvert --to html '{project_notebook_path}' --output '{temp_path}'", shell=True)
    
    
    title_line = sp.run(f"grep '<h1' '{temp_path}'", shell=True, capture_output=True).stdout.decode().split('\n')[0]
    project_name = title_line[title_line.index('>')+1:]
    project_name = project_name[:project_name.index('<')]
    print(f'Project Name: {project_name}')

    project_base_path = project_name
    while len(project_base_path) > max_base_filename_length:
        project_base_path = ' '.join(project_base_path.split(' ')[:-1])
    
    if not project_base_path:
        print(f"\n\n\n\n\tWarning: Project '{project_name}' Name exceeds recommended length\n\n\n\n")
        project_base_path = project_name
    project_path = f'{os.getcwd()}/projects/{project_base_path}.html'
    
    assert project_path not in project_paths
    os.rename(temp_path, project_path)
    
    project_names.append(project_name)
    project_paths.append(project_path)
    print('\n')


# In[32]:


index_html_path = 'index.html'


# In[33]:


index_html_lines = open(index_html_path).readlines()


# In[34]:


project_list_index_start = index_html_lines.index('<ul>\n') + 1
project_list_index_end = index_html_lines.index('</ul>\n')


# In[35]:


new_project_list =  [f'\t<li><a href="projects/{os.path.basename(html_path)}">{name}</a></li>\n' for name, html_path in zip(project_names, project_paths)]


# In[36]:


new_project_list


# In[37]:


index_html_lines = index_html_lines[:project_list_index_start] + new_project_list + index_html_lines[project_list_index_end:]


# # Copying Resume and Updating Links

# In[38]:


assert shutil.copy(metadata['Resume'], f"projects/{os.path.basename(metadata['Resume'])}")


# In[39]:


index_html_lines


# In[40]:


tag_dict = {tag: metadata[tag] for tag in ['Resume', 'LinkedIn', 'GitHub']}
tag_dict['Resume'] = f"projects/{os.path.basename(tag_dict['Resume'])}"


# In[41]:


for i, line in enumerate(index_html_lines):
    for tag in tag_dict:
        prefix = f"<a id='{tag}' href='"
        if line.startswith(prefix):
            print(line.strip())
            new_line = prefix + tag_dict[tag] + line[len(prefix) + line[len(prefix):].index("'"):]
            print(new_line)
            index_html_lines[i] = new_line
    
    if line.startswith(prefix):
        del tag_dict[tag]


# # Writing Updated Index File

# In[42]:


with open(index_html_path, 'w') as outfile:
    outfile.write(''.join(index_html_lines))


# In[ ]:





# In[ ]:




