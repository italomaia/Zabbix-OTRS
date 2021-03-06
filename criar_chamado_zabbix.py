# encoding: utf-8
from otrs.ticket.template import GenericTicketConnectorSOAP
from otrs.client import GenericInterfaceClient
from otrs.ticket.objects import Ticket, Article, DynamicField, Attachment

import mimetypes
import base64
import argparse
import time
import re

# Parse das opcoes de linha de comando
parser = argparse.ArgumentParser(description='Criar um ticket.')
parser.add_argument('--otrs', dest='server', help='OTRS server address, ex: 10.20.19.47')
parser.add_argument('--webservice', dest='webservice', default='ZabbixOTRS', help='OTRS Web Servcice')
parser.add_argument('--user', dest='user', default='otrs.isaac', help='OTRS user')
parser.add_argument('--pass', dest='password', default='pass.isaac', help='OTRS pass')
parser.add_argument('--customer', dest='customer', help='Customer')
parser.add_argument('--title', dest='title', help='Titulo do chamado')
parser.add_argument('--desc', dest='descricao', help='Descricao')
parser.add_argument('--fila', dest='fila', help='Fila de atendimento')
parser.add_argument('--servico', dest='servico', help='Servico de abertura')
parser.add_argument('--sla', dest='sla', help='SLA')
parser.add_argument('--triggerid', dest='triggerid', help='Trigger ID do zabbix')
parser.add_argument('--host', dest='host', help='Nome do host no zabbix')
parser.add_argument('--status', dest='status', help='Indisponibilidade')
parser.add_argument('--timeunit', dest='timeunit', help='Unidade de tempo do ticket')
args = parser.parse_args()

#print(args)

# Conexao com o OTRS
server_uri = 'http://'+args.server+'/'
webservice_name = args.webservice
client = GenericInterfaceClient(server_uri, tc=GenericTicketConnectorSOAP(webservice_name))
client.tc.SessionCreate(user_login=args.user, password=args.password)

#Criando o ticket
t = Ticket(State='Aberto', Priority='3 normal', Queue=args.fila,
           Title=args.title.decode('UTF8'), CustomerUser=args.customer,
           Type='Incidente', Service=args.servico, SLA=args.sla, TimeUnit=args.timeunit)
a = Article(Subject=args.title.decode('UTF8'), Body=args.descricao.decode('UTF8'), Charset='UTF8',
            MimeType='text/plain')

t_id, t_number = client.tc.TicketCreate(t, a, None, None)
print('Ticket criado: '+str(t_number))
print('Ticket criado: '+str(t_number)+'::'+args.title)

# Ticket em atendimento
t_upd = Ticket(State='Em atendimento')

new_article = Article(Subject='Em atendimento', Body='Analisando o incidente.', Charset='UTF8',
                      MimeType='text/plain')
client.tc.TicketUpdate(t_id, ticket=t_upd,article=new_article, attachments=None)
