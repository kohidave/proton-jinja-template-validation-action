from pathlib import Path

class TemplateDir:            
    @staticmethod
    def is_path_template_dir(path):
        return path.find("/instance_infrastructure/") != -1 or \
               path.find("/pipeline_infrastructure/") != -1 or \
               path.find("/infrastructure/") != -1 or \
               path.find("/schema/") != -1 or path.find("/spec/") != -1

    @staticmethod
    def top_level_template_dir(path):
        instance_infra_folder_index  = path.find("/instance_infrastructure/")
        pipeline_infra_folder_index = path.find("/pipeline_infrastructure/")
        environment_infra_folder_index = path.find("/infrastructure/")
        schema_folder_index = path.find("/schema/")
        spec_folder_index = path.find("/spec/")

        if instance_infra_folder_index != -1:
            return path[0:instance_infra_folder_index]
        if pipeline_infra_folder_index != -1:
            return path[0:pipeline_infra_folder_index]     
        if schema_folder_index != -1:
            return path[0:schema_folder_index]     
        if environment_infra_folder_index != -1:
            return path[0:environment_infra_folder_index]                 
        if spec_folder_index != -1:
            return path[0:spec_folder_index]
        return ""

    # from_paths returns a collection of TemplateDirs from a list of paths. 
    # It will filter out non-template paths, remove duplicate template paths,
    # and return a collection of TemplateDir objects
    @staticmethod
    def from_paths(paths):
        template_files = set(filter(TemplateDir.is_path_template_dir, paths))
        template_dirs = set(map(TemplateDir.top_level_template_dir, template_files))
        return set(map(lambda template_path: TemplateDir("", template_path), template_dirs))

    def __init__(self, repo_path, template_path):
        self.repo_path = repo_path
        self.template_path = template_path
        self.path = repo_path+template_path

    def schema_path(self):
       return self.path + "/schema/schema.yaml"

    def sample_outputs_path(self):
        return self.path + "/spec/sample-outputs.yaml"

    def sample_spec_path(self):
        return self.path + "/spec/spec.yaml"

    def instance_infra_relative_path(self):
        return "/instance_infrastructure/cloudformation.yaml"

    def pipeline_infra_relative_path(self):
        return "/pipeline_infrastructure/cloudformation.yaml"

    def environment_infra_relative_path(self):
        return "/infrastructure/cloudformation.yaml"

    def instance_infra_path(self):
        return self.path + self.instance_infra_relative_path()

    def pipeline_infra_path(self):
        return self.path + self.pipeline_infra_relative_path()

    def environment_infra_path(self):
        return self.path + self.environment_infra_relative_path()        
