from django import template
from django.template.base import Node, NodeList

register = template.Library()

class IsCategoryChildNode(Node):
	"""
	IfEqual-based tag to test if provided category A is a parent of category B
	"""
	child_nodelists = ('nodelist_true', 'nodelist_false')

	def __init__(self, current_category, active_category, nodelist_true, nodelist_false, negate):
		self.current_category, self.active_category = current_category, active_category
		self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
		self.negate = negate

	def __repr__(self):
		return "<IsCategoryChildNode>"

	def render(self, context):
		current_category = self.current_category.resolve(context, True)
		active_category = self.active_category.resolve(context, True)
		#raise ValueError((current_category, current_category.get_descendants(), active_category))
		truelist = self.nodelist_true
		falselist = self.nodelist_false
		if self.negate:
			falselist = self.nodelist_true
			truelist = self.nodelist_false
		if active_category in current_category.get_descendants():
			return self.nodelist_true.render(context)
		return self.nodelist_false.render(context)

def do_iscategorychild(parser, token, negate):
	bits = list(token.split_contents())
	if len(bits) != 3:
		raise TemplateSyntaxError("%r takes two arguments" % bits[0])
	end_tag = 'end' + bits[0]
	nodelist_true = parser.parse(('else', end_tag))
	token = parser.next_token()
	if token.contents == 'else':
		nodelist_false = parser.parse((end_tag,))
		parser.delete_first_token()
	else:
		nodelist_false = NodeList()
	val1 = parser.compile_filter(bits[1])
	val2 = parser.compile_filter(bits[2])
	return IsCategoryChildNode(val1, val2, nodelist_true, nodelist_false, negate)

#@register.tag
def iscategorychild(parser, token):
	return do_iscategorychild(parser, token, False)
iscategorychild = register.tag(iscategorychild)

#@register.tag
def isnotcategorychild(parser, token):
	return do_iscategorychild(parser, token, True)
isnotcategorychild = register.tag(isnotcategorychild)