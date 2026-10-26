from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Prefetch
from dcim.models import Site, Location, Rack, Device

class CompactRackSpaceView(PermissionRequiredMixin, View):
    permission_required = 'dcim.view_rack'

    def get(self, request):
        selected_site_slug = request.GET.get('site')
        selected_location_id = request.GET.get('location')

        # Базовые списки для фильтров
        all_sites = Site.objects.filter(racks__isnull=False).distinct().order_by('name')
        
        # ДИНАМИЧЕСКИЙ ФИЛЬТР: Если площадка выбрана, показываем только её локации
        all_locations = Location.objects.filter(racks__isnull=False).distinct().order_by('name')
        if selected_site_slug:
            all_locations = all_locations.filter(site__slug=selected_site_slug)

        # Запрос площадок для рендеринга
        sites_query = Site.objects.filter(racks__isnull=False).distinct().order_by('name')
        if selected_site_slug:
            sites_query = sites_query.filter(slug=selected_site_slug)

        devices_prefetch = Prefetch(
            'devices',
            queryset=Device.objects.exclude(position__isnull=True).only('id', 'name', 'rack_id', 'position'),
            to_attr='prefetched_devices'
        )

        grouped_data = []
        
        for site in sites_query:
            site_info = {
                'name': site.name,
                'locations': []
            }
            
            locations_query = Location.objects.filter(site=site, racks__isnull=False).distinct().order_by('name')
            if selected_location_id:
                locations_query = locations_query.filter(id=selected_location_id)
            
            if not selected_location_id:
                root_racks = Rack.objects.filter(site=site, location__isnull=True).order_by('name').prefetch_related(devices_prefetch)
                if root_racks.exists():
                    site_info['locations'].append({
                        'name': 'Без локации',
                        'racks': self._get_racks_data(root_racks)
                    })
                
            for loc in locations_query:
                loc_racks = Rack.objects.filter(location=loc).order_by('name').prefetch_related(devices_prefetch)
                site_info['locations'].append({
                    'name': loc.name,
                    'racks': self._get_racks_data(loc_racks)
                })
                
            if site_info['locations']:
                grouped_data.append(site_info)

        return render(request, 'netbox_compact_rackspace/dashboard.html', {
            'grouped_data': grouped_data,
            'all_sites': all_sites,
            'all_locations': all_locations,
            'selected_site': selected_site_slug,
            'selected_location': selected_location_id,
        })

    def _get_racks_data(self, racks):
        racks_list = []
        for rack in racks:
            total_u = rack.u_height
            device_map = {d.position: d for d in rack.prefetched_devices}
            
            units = []
            for u in range(total_u, 0, -1):
                device = device_map.get(u)
                if device:
                    units.append({
                        'u_num': u,
                        'is_occupied': True,
                        'device_name': device.name,
                        'device_url': f'/dcim/devices/{device.pk}/'
                    })
                else:
                    units.append({
                        'u_num': u,
                        'is_occupied': False
                    })
            
            occupied_count = sum(1 for unit in units if unit['is_occupied'])
            utilization = int((occupied_count / total_u) * 100) if total_u > 0 else 0
            
            if utilization < 40:
                header_color = '#28a745'
            elif utilization < 80:
                header_color = '#ffc107'
            else:
                header_color = '#dc3545'
                
            racks_list.append({
                'id': rack.pk,
                'name': rack.name,
                'total_u': total_u,
                'utilization': utilization,
                'header_color': header_color,
                'units': units
            })
        return racks_list
