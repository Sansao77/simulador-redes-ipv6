from django.shortcuts import render
from django.db import IntegrityError
from .models import Device, Router
import ipaddress

def home(request):
    devices = Device.objects.all()
    routers = Router.objects.all()
    return render(request, 'home.html', {'devices': devices, 'routers': routers})

def simulate_network(request):
    # Lógica para simular comunicação IPv6
    devices = Device.objects.all()
    routers = Router.objects.all()
    simulation_result = ["Exemplo de resultado de simulação"]

    for device in devices:
        if device.connected_to:
            simulation_result.append(f"{device.name} comunica-se via {device.connected_to.name}")
    
    return render(request, 'simulation.html', {'result': simulation_result})

def create_demo_network():
    try:
        # Criando roteadores (ou obtendo, se já existirem)
        router1, _ = Router.objects.get_or_create(name="Router1", defaults={"ipv6_address": "2001:db8:1::1"})
        router2, _ = Router.objects.get_or_create(name="Router2", defaults={"ipv6_address": "2001:db8:2::1"})
        router3, _ = Router.objects.get_or_create(name="Router3", defaults={"ipv6_address": "2001:db8:3::1"})
        router4, _ = Router.objects.get_or_create(name="Router4", defaults={"ipv6_address": "2001:db8:4::1"})

        # Conectando roteadores em uma topologia mais intrincada
        if not router1.connected_routers.filter(id=router2.id).exists():
            router1.connected_routers.add(router2)
        if not router2.connected_routers.filter(id=router3.id).exists():
            router2.connected_routers.add(router3)
        if not router3.connected_routers.filter(id=router4.id).exists():
            router3.connected_routers.add(router4)
        if not router4.connected_routers.filter(id=router1.id).exists():
            router4.connected_routers.add(router1)
        if not router2.connected_routers.filter(id=router4.id).exists():
            router2.connected_routers.add(router4)  # Adicionando mais complexidade

        # Criando dispositivos e associando a diferentes roteadores
        devices = []
        devices.append(Device.objects.get_or_create(name="Device1", defaults={"ipv6_address": "2001:db8:1::100", "connected_to": router1})[0])
        devices.append(Device.objects.get_or_create(name="Device2", defaults={"ipv6_address": "2001:db8:2::100", "connected_to": router2})[0])
        devices.append(Device.objects.get_or_create(name="Device3", defaults={"ipv6_address": "2001:db8:3::100", "connected_to": router3})[0])
        devices.append(Device.objects.get_or_create(name="Device4", defaults={"ipv6_address": "2001:db8:4::100", "connected_to": router4})[0])
        devices.append(Device.objects.get_or_create(name="Device5", defaults={"ipv6_address": "2001:db8:1::101", "connected_to": router1})[0])
        devices.append(Device.objects.get_or_create(name="Device6", defaults={"ipv6_address": "2001:db8:3::102", "connected_to": router3})[0])

        # Retornando os dados da rede
        return {"routers": [router1, router2, router3, router4], "devices": devices}

    except IntegrityError as e:
        print(f"Erro de integridade: {e}")
        return {"routers": [], "devices": []}

def demo(request):
    # Configura e inicializa uma rede demo
    network = create_demo_network()
    return render(request, "demo.html", {"network": network})

def simulate_communication(source_ip, dest_ip, routers):
    source_network = ipaddress.ip_network(source_ip + "/64", strict=False)
    dest_network = ipaddress.ip_network(dest_ip + "/64", strict=False)

    path = []

    if source_network != dest_network:
        # Encaminhar via roteadores
        for router in routers:
            if ipaddress.ip_address(dest_ip) in ipaddress.ip_network(router.ipv6_address + "/64"):
                path.append(f"Encaminhado via {router.name}")
                break

    path.append(f"Mensagem entregue de {source_ip} para {dest_ip}")
    return path

def simulate_demo(request):
    routers = Router.objects.all()
    path = simulate_communication("2001:db8:1::100", "2001:db8:2::100", routers)
    return render(request, "simulate_demo.html", {"path": path})
