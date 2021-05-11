from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import AzureAccessKey,DownloadPath
from azure.storage.blob import BlobServiceClient,ContainerClient

# Create your views here.

class Index(View):
    template_name = 'app/list_containers.html'
    def get(self,request):
        if not request.session.get('conn_str'):
            try:
                conn_str = AzureAccessKey.objects.get(name='AZURE_STORAGE_CONNECTION_STRING').connection_string
                request.session['conn_str'] = conn_str
            except:
                return HttpResponse('<h1>AZURE_STORAGE_CONNECTION_STRING variable not set</h1><p>Please set the variable in django admin panel in AzureAccessKey table</p>')
        context = {}
    
        blob_service = BlobServiceClient.from_connection_string(conn_str=request.session['conn_str'])
        containers = blob_service.list_containers()
        containers=list(containers)
        context['containers'] = containers
        return render(request,template_name=self.template_name,context=context)


class ViewContainerFiles(View):
    template_name = 'app/list_files.html'
    def get(self,request,container_name):
        container_client= ContainerClient.from_connection_string(conn_str=request.session['conn_str'], container_name=container_name)
        download_paths = DownloadPath.objects.all()
        context = {}
        blob_list = container_client.list_blobs()
        blob_list = list(blob_list)
        context['container'] = container_name
        context['files'] = blob_list
        context['download_paths'] = download_paths
        return render(request,self.template_name,context)

    def post(self,request,container_name):
        blobs=request.POST.getlist('files')
        blob_service = BlobServiceClient.from_connection_string(conn_str=request.session['conn_str'])
        download_path = request.POST.get('downloadPath')
        for blob in blobs:
            blob_client = blob_service.get_blob_client(container_name, blob)
            print("\nDownloading blob to \n\t" + download_path)
            with open("{}/{}".format(download_path,blob), "wb") as my_blob:
                blob_data = blob_client.download_blob()
                blob_data.readinto(my_blob)
            my_blob.close()
        return redirect('view_files',container_name=container_name)
        